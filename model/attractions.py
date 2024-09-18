import json
import os

from sqlalchemy import text

CLOUDFRONT_DOMAIN = os.getenv('CLOUDFRONT_DOMAIN')
                    
async def getAttractions(db, start_index, items_per_page, keyword,spots_redis):
    try:
        cache_key = f"attractions:{keyword}:{start_index}:{items_per_page}"
        
        redis_data = spots_redis.get(cache_key)
      
        
        if redis_data:
            data = json.loads(redis_data)
            return data 
        total_num_stmt = text("""
            SELECT COUNT(*) 
            FROM spots 
            WHERE MRT = :keyword OR name LIKE :keyword_like
        """)
        total_num_result = await db.execute(total_num_stmt, {'keyword': keyword, 'keyword_like': '%' + keyword + '%'})
        total_num = total_num_result.scalar()

        if total_num == 0:
            return {"results": None, "total_page": 0}
        
        total_page = total_num / items_per_page

        select_stmt = text("""
            SELECT spots.*, 
                GROUP_CONCAT(CONCAT(:cloudfront_domain, '/', SUBSTRING_INDEX(spot_imgs.images, '/', -1)) SEPARATOR ',') as image_urls
            FROM spots 
            LEFT JOIN spot_imgs ON spots.id = spot_imgs.img_id
            WHERE spots.MRT = :keyword OR spots.name LIKE :keyword_like
            GROUP BY spots.id
            LIMIT :start_index, :items_per_page
        """)
        
        result = await db.execute(select_stmt, {
            'cloudfront_domain': CLOUDFRONT_DOMAIN, 
            'keyword': keyword, 
            'keyword_like': '%' + keyword + '%', 
            'start_index': start_index, 
            'items_per_page': items_per_page
        })
        
        results = result.all()
        results_list = []
        
        for row in results:
            row_dict = row._asdict()
            if row_dict["image_urls"]:
                row_dict["images"] = row_dict["image_urls"].split(',')
                del row_dict["image_urls"]
            else:
                row_dict["images"] = []
            results_list.append(row_dict)
        

        data = {"results": results_list, "total_page": total_page}
                
        spots_redis.set(cache_key, json.dumps(data), ex=3600)
    
        return data
    except Exception as e:
        print(f"Unhandled exception: {e}")
        return {"results": "error", "total_page": 0}

import json
import redis
import os
spots_redis = redis.Redis(host="redis", port=6379, db=0)

CLOUDFRONT_DOMAIN = os.getenv('CLOUDFRONT_DOMAIN')
                    
def getAttractions(db_pool, start_index, items_per_page, keyword):
    try:
        cache_key = f"attractions:{keyword}:{start_index}:{items_per_page}"
        
        redis_data = spots_redis.get(cache_key)
      
        
        if redis_data:
            data = json.loads(redis_data)
            return data 
        
        with db_pool.get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                
                cursor.execute("SELECT COUNT(*) FROM spots WHERE MRT = %s OR name LIKE %s", (keyword, '%' + keyword + '%'))
                total_num = cursor.fetchone()["COUNT(*)"]
              
                
                if total_num == 0:
                    return {"results": None, "total_page": 0}
                
                total_page = total_num / 12
                
                cursor.execute("""
                               SELECT spots.*,
                                    GROUP_CONCAT(CONCAT(%s, '/', SUBSTRING_INDEX(spot_imgs.images, '/', -1)) SEPARATOR ',') as image_urls
                                FROM spots 
                                LEFT JOIN spot_imgs ON spots.id = spot_imgs.img_id
                                WHERE spots.MRT = %s OR spots.name LIKE %s
                                GROUP BY spots.id
                                LIMIT %s, %s""",
                                (CLOUDFRONT_DOMAIN,keyword, '%' + keyword + '%', start_index, items_per_page))
                
                results = cursor.fetchall()
                for result in results:
                    if result["image_urls"]:
                        result["images"] = result["image_urls"].split(',')
                    else:
                        result["images"] = []
                # for result in results:
                #     id = result["id"]

                #     cursor.execute("SELECT images FROM spot_imgs WHERE img_id = %s", (id,))
                #     img_urls = [f"{CLOUDFRONT_DOMAIN}/{row["images"].split('/')[-1]}" for row in cursor.fetchall()]

                #     result["images"] = img_urls
                
                data = {"results": results, "total_page": total_page}
                
                spots_redis.set(cache_key, json.dumps(data), ex=3600)
            
                return data
    except Exception as e:
        print(f"Unhandled exception: {e}")
        return {"results": "error", "total_page": 0}

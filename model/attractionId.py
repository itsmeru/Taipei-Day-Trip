import json
import os 
from sqlalchemy import  text


CLOUDFRONT_DOMAIN = os.getenv('CLOUDFRONT_DOMAIN')

async def getAttractionId(db, attractionId,attraction_redis):
    try:
        cache_key = f"attractionID:{attractionId}"
        redis_data = attraction_redis.get(cache_key)
        if redis_data:
            data = json.loads(redis_data)
            return data
        stmt = text("""
            SELECT spots.*, 
                GROUP_CONCAT(CONCAT(:cloudfront_domain, '/', SUBSTRING_INDEX(spot_imgs.images, '/', -1)) SEPARATOR ',') as image_urls
            FROM spots
            LEFT JOIN spot_imgs ON spots.id = spot_imgs.img_id
            WHERE spots.id = :attraction_id
            GROUP BY spots.id
        """)
        results = await db.execute(stmt, {'cloudfront_domain': CLOUDFRONT_DOMAIN, 'attraction_id': attractionId})  
        result = results.first()._asdict()

        if result["image_urls"]:
            result["images"] = result["image_urls"].split(",")
            del result["image_urls"]

        data = {"data": result}
        attraction_redis.set(cache_key, json.dumps(data), ex=3600)
        
        return data
    except Exception as e:
        print(f"Unhandled exception: {e}")
        return "error"
       
    
  
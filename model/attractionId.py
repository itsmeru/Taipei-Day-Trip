import json
import os 

CLOUDFRONT_DOMAIN = os.getenv('CLOUDFRONT_DOMAIN')

def getAttractionId(db_pool, attractionId,attraction_redis):
    try:
        cache_key = f"attractionID:{attractionId}"
        redis_data = attraction_redis.get(cache_key)
        if redis_data:
            data = json.loads(redis_data)
            return data
        with db_pool.get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("""
                        SELECT spots.*, 
                            GROUP_CONCAT(CONCAT(%s, '/', SUBSTRING_INDEX(spot_imgs.images, '/', -1)) SEPARATOR ',') as image_urls
                        FROM spots
                        LEFT JOIN spot_imgs ON spots.id = spot_imgs.img_id
                        WHERE spots.id = %s
                        GROUP BY spots.id
                        """,(CLOUDFRONT_DOMAIN,attractionId,))
                
                spots_data = cursor.fetchone()
                if not spots_data:
                    data = {"error": True, "message": "找不到此景點"}
                    return None
                
                if spots_data["image_urls"]:
                    spots_data["images"] = spots_data["image_urls"].split(',')
                else:
                    spots_data["images"] = []

                data = {"data":spots_data}

                attraction_redis.set(cache_key, json.dumps(data),ex=3600)
                return data
    except Exception as e:
        print(f"Unhandled exception: {e}")
        return "error"


       
    
  
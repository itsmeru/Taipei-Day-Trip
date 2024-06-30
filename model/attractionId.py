import json
import redis
attraction_redis = redis.Redis(host="localhost", port=6379, db=1)

def getAttractionId(db_pool, attractionId):
    try:
        redis_data = attraction_redis.get(attractionId)
        if redis_data:
            data = json.loads(redis_data)
            print("SUCESSSS")
            return data
        with db_pool.get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM spots WHERE id = %s", (attractionId,))
                spots_data = cursor.fetchone()
                if not spots_data:
                    data = {"error": True, "message": "找不到此景點"}
                    return None
                
                cursor.execute("SELECT images FROM spot_imgs WHERE img_id = %s", (attractionId,))
                img_urls = [row["images"] for row in cursor.fetchall()]
                spots_data["images"] = img_urls
                data = {"data":spots_data}
                attraction_redis.set(attractionId, json.dumps(data))
                return data
    except Exception as e:
        print(f"Unhandled exception: {e}")
        return "error"


       
    
  
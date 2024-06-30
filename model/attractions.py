import json
import redis
spots_redis = redis.Redis(host="localhost", port=6379, db=2)
def getAttractions(db_pool,start_index, items_per_page, keyword):
    try:
        cache_key = f"attractions:{keyword}:{start_index}:{items_per_page}"
        redis_data = spots_redis.get(cache_key)
        if redis_data:
            data = json.loads(redis_data)
            return data 
        
        with db_pool.get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT  COUNT(*)  FROM spots WHERE MRT = %s OR name LIKE %s ", (keyword, '%' + keyword + '%'))
                results = cursor.fetchall()
                total_num = total_num = results[0]["COUNT(*)"]
                total_page = total_num / 12
                if not results:
                    data = {"results": None, "total_page": 0}
                    return data
                
                cursor.execute("SELECT * FROM spots WHERE MRT = %s OR name LIKE %s LIMIT %s,%s", (keyword, '%' + keyword + '%', start_index, items_per_page))
                results = cursor.fetchall()
                for result in results:
                    id = result["id"]
                    cursor.execute("SELECT images FROM spot_imgs WHERE img_id = %s", (id,))
                    img_urls = [row["images"] for row in cursor.fetchall()]
                    result["images"] = img_urls
                    data = {"results": results, "total_page": total_page}
                    spots_redis.set(cache_key, json.dumps(data))
                return data
    except Exception as e:
        print(f"Unhandled exception: {e}")
        data = {"results": "error", "total_page": 0}
        return data

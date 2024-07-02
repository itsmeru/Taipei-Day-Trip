from http.client import HTTPException

import redis
schedule_redis = redis.Redis(host="localhost", port=6379, db=0)

def getBookInfo(db_pool,cart,tokenData):
    try:
        token = tokenData["data"]
        if token is None:
            return "forbidan"
        user_id = tokenData["data"]["id"]
       
        with db_pool.get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("""
                        INSERT INTO schedule (user_id, attraction_id, date, time, price)
                        VALUES (%s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        attraction_id = VALUES(attraction_id),
                        date = VALUES(date),
                        time = VALUES(time),
                        price = VALUES(price)
                        """, (user_id, cart["attraction_id"], cart["date"], cart["time"], cart["price"]))
                cache_key = f"member:{user_id}"
                schedule_redis.delete(cache_key)
                con.commit()
                datas = {"ok":True}
                return datas
    except HTTPException as http_exc:
        return http_exc
    except Exception as e:
        print(e)
        return "error"
        
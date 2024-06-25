from http.client import HTTPException
from model.getUser import getUser


def getBookInfo(db_pool,data):
    try:
        token = data["token"]
        
        if getUser(token) == None:
            return "forbidan"

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
                        """, (data["user_id"], data["attraction_id"], data["date"], data["time"], data["price"]))

                con.commit()
                print("OK")
        datas = {"ok":True}
        return datas
    except HTTPException as http_exc:
        return http_exc
    except Exception as e:
        print(e)
        return "error"
        
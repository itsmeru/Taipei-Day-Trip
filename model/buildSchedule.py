from http.client import HTTPException
from model.getUser import getUser


def getBookInfo(db_pool,data):
    try:
        token = data["token"]
        
        if getUser(token) == None:
            return "forbidan"

        with db_pool.get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("insert into schedule(user_id,attraction_id,date,time,price)values(%s,%s,%s,%s,%s)",(data["user_id"],data["attraction_id"],data["date"],data["time"],data["price"]))
                con.commit()
        datas = {"ok":True}
        return datas
    except HTTPException as http_exc:
        return http_exc
    except Exception as e:
        print(e)
        return "error"
        
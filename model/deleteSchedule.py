from model.getUser import getUser

def getDeleteSchedule(db_pool,user_id,attraction_id,token):
    data = getUser(token)
    if data["data"] == None or data["data"]["id"] != user_id:
            return "forbidan"
    try:
        with db_pool.get_connection() as con:
            with con.cursor() as cursour:
                cursour.execute("delete from schedule where attraction_id = %s and user_id = %s",(attraction_id,user_id))
                con.commit()
                data = {"ok":True}
                return data
    except Exception as e:
        return "error"
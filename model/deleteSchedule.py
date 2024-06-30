from model.getUser import getUser
import redis
schedule_redis = redis.Redis(host="redis", port=6379, db=0)

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
                schedule_redis.delete(user_id)
                return data
    except Exception as e:
        return "error"
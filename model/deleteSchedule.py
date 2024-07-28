from model.getUser import getUser
from models import Schedule
from sqlalchemy import delete

async def getDeleteSchedule(db,user_id,attraction_id,token,schedule_redis):
    data = getUser(token)
    if data["data"] == None or data["data"]["id"] != user_id:
            return "forbidan"
    try:
        stmt = delete(Schedule).where(Schedule.user_id == user_id, Schedule.attraction_id == attraction_id)
        await db.execute(stmt)
        await db.commit()
        data = {"ok":True}
        cache_key = f"member:{user_id}"
        schedule_redis.delete(cache_key)
        return data
    except Exception as e:
        print(f"Unhandled exception: {e}")
        return "error"
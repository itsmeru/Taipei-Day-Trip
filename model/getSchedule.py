import datetime

from sqlalchemy import select
from model.attractionId import getAttractionId
from model.getUser import getUser
from models import Schedule 
import json

async def getSchedule(db,token,schedule_redis):
    data = getUser(token)
    if data == "error" or data is None:
            return "forbidan"
    user_id = data["data"]["id"]
    try:
        cache_key = f"member:{user_id}"
        cart_data = schedule_redis.get(cache_key)
        if cart_data:
            cart = json.loads(cart_data)
            return cart
        else:
            stmt = select(Schedule).filter(Schedule.user_id == user_id)
            results = await db.execute(stmt)
            result = results.scalar_one_or_none() # result 是一个 Schedule 實體物件
            if result:
                attraction_id = result.attraction_id
                date = result.date
                if isinstance(date, datetime.date):
                    date = date.strftime("%Y-%m-%d")
                time = result.time
                price = result.price

                datas = await getAttractionId(db, attraction_id,schedule_redis)
                attractionInfo = datas["data"]
                name = attractionInfo["name"]
                address = attractionInfo["address"]
                images = attractionInfo["images"][0]
                info = {"data":{
                    "attractions":{
                        "id": attraction_id,
                        "name": name,
                        "address": address,
                        "images": images
                    },
                    "date": date,
                    "time": time,
                    "price": price
                }}
                cache_key = f"member:{user_id}"
                schedule_redis.set(cache_key,json.dumps(info))
                return info
            else:
                return None
    except Exception as e:
        print(f"Unhandled exception: {e}")
        return "error"

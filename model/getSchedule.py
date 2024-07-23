import datetime
from model.attractionId import getAttractionId
from model.getUser import getUser

import json

def getSchedule(db_pool,token,schedule_redis):
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
            with db_pool.get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    cursor.execute("select * from schedule where user_id = %s",(user_id,))
                    result = cursor.fetchone()
                    if result:
                        attraction_id = result["attraction_id"]
                        date = result["date"]
                        if isinstance(date, datetime.date):
                            date = date.strftime("%Y-%m-%d")
                        time = result["time"]
                        price = result["price"]
                        datas = getAttractionId(db_pool, attraction_id)
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
        return "error"

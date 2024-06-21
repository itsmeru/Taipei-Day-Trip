import datetime
from model.attractionId import getAttractionId
from model.getUser import getUser


def getSchedule(db_pool,token):
    data = getUser(token)
    if data["data"] == None:
            return "forbidan"
    user_id = data["data"]["id"]
    try:
        with db_pool.get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("select * from schedule where user_id = %s",(user_id,))
                results = cursor.fetchall()
                if results:
                    bookInfo = []
                    for result in results:
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
                        bookInfo.append(info)
                    return bookInfo
                else:
                    return None
    except Exception as e:
        return "error"

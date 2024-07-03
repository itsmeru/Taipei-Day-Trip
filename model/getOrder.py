import datetime

from model.getUser import getUser

def getOrder(token,db_pool,orderNumber):
    data = getUser(token)
    if data == "error" or data is None:
            return "forbidan"
    try:
        with db_pool.get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("select * from orders where order_number = %s",(orderNumber,))
                order_result = cursor.fetchall()
                if order_result:
                    order_results = order_result[0]
                    order_status = order_results["status"]
                    if order_status == "PAID":
                        status = 1
                    else:
                        status = 0
                    date = order_results["trip_date"]
                    if isinstance(date, datetime.date):
                        date = date.strftime("%Y-%m-%d")
                    data = {
                            "data": {
                                "number": orderNumber,
                                "price":order_results["price"] ,
                                "trip": {
                                "attraction": {
                                    "id": order_results["attraction_id"],
                                    "name": order_results["attraction_name"],
                                    "address": order_results["attraction_address"],
                                    "image": order_results["attraction_image"]
                                },
                                "date": date,
                                "time": order_results["trip_time"]
                                },
                                "contact": {
                                "name": order_results["contact_name"],
                                "email": order_results["contact_email"],
                                "phone": order_results["contact_phone"]
                                },
                                "status": status
                            }
                        }
                    return data
                else:
                    data = {"data":None}
                    return data
    except Exception as e:
        print(e)
        return "error"
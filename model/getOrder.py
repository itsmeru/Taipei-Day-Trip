from datetime import datetime,date
from models import Order

from model.getUser import getUser
from sqlalchemy import select
async def getOrder(token,db,orderNumber):
    data = getUser(token)
    if data == "error" or data is None:
            return "forbidan"
    try:
        result = await db.execute(select(Order).filter(Order.order_number == orderNumber))
        order_result = result.scalars().first()
        
        if order_result:
            order_status = order_result.status
            status = 1 if order_status == "PAID" else 0

            trip_date = order_result.trip_date
            if isinstance(trip_date, date):
                trip_date = trip_date.strftime("%Y-%m-%d")

            data = {
                "data": {
                    "number": orderNumber,
                    "price": order_result.price,
                    "trip": {
                        "attraction": {
                            "id": order_result.attraction_id,
                            "name": order_result.attraction_name,
                            "address": order_result.attraction_address,
                            "image": order_result.attraction_image
                        },
                        "date": trip_date,
                        "time": order_result.trip_time
                    },
                    "contact": {
                        "name": order_result.contact_name,
                        "email": order_result.contact_email,
                        "phone": order_result.contact_phone
                    },
                    "status": status
                }
            }
            return data
        else:
            return {"data": None}
    except Exception as e:
        print(f"Error: {e}")
        return "error"
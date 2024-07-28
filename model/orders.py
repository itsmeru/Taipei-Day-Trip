from datetime import datetime
from sqlalchemy import select
import httpx

from model.getUser import getUser
from models import Order

async def getOrders(db, token: str, bookInfo, order_data):
    tokenData = getUser(token)
    if tokenData == "error" or tokenData is None:
        return "forbidan"
    
    user_id = tokenData["data"]["id"]
    
    result = await db.execute(
            select(Order).filter(Order.user_id == user_id, Order.status.in_(['UNPAID', 'FAILED']))
        )
    existing_order = result.scalars().first()

    if existing_order:
        existing_order.price = bookInfo.order.price
        existing_order.attraction_id = bookInfo.order.trip.attraction.id
        existing_order.attraction_name = bookInfo.order.trip.attraction.name
        existing_order.attraction_address = bookInfo.order.trip.attraction.address
        existing_order.attraction_image = bookInfo.order.trip.attraction.image
        existing_order.trip_date = bookInfo.order.trip.date
        existing_order.trip_time = bookInfo.order.trip.time
        existing_order.contact_name = bookInfo.order.contact.name
        existing_order.contact_email = bookInfo.order.contact.email
        existing_order.contact_phone = bookInfo.order.contact.phone
        order_id = existing_order.id
    else:
        new_order = Order(
            user_id=user_id,
            price=bookInfo.order.price,
            attraction_id=bookInfo.order.trip.attraction.id,
            attraction_name=bookInfo.order.trip.attraction.name,
            attraction_address=bookInfo.order.trip.attraction.address,
            attraction_image=bookInfo.order.trip.attraction.image,
            trip_date=bookInfo.order.trip.date,
            trip_time=bookInfo.order.trip.time,
            contact_name=bookInfo.order.contact.name,
            contact_email=bookInfo.order.contact.email,
            contact_phone=bookInfo.order.contact.phone,
            status='UNPAID'
        )
        db.add(new_order)
        await db.commit()
        order_id = new_order.id

    order_status, request_time, data = await sendPrime(order_data, token)
    print(order_status,data)
    
    if order_status == "API error":
        await updateOrderStatus(db, order_id, "FAILED", order_number=data["order_number"], cancelled_at=request_time)
        payment_result = {
            "data": {
                "number": data["order_number"],
                "payment": {
                    "status": data["status"],
                    "message": "付款失敗"
                }
            }
        }
        return {"error": False, "payment_result": payment_result}
    elif order_status in ["request error", "error"]:
        return {"error": True, "data": data}
    else:
        await updateOrderStatus(db, order_id, "PAID", order_number=data["order_number"], paid_at=request_time)
        payment_result = {
            "data": {
                "number": data["order_number"],
                "payment": {
                    "status": data["status"],
                    "message": "付款成功"
                }
            }
        }
        return {"error": False, "payment_result": payment_result}

async def sendPrime(order_data, token):
    tap_pay_url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{token}",
        "x-api-key": "partner_71JD0IlN4Td4dKlAno18sKBDji9PScQ0oM0a0zkj7ZNpNxiSiG3hFzLm",
    }
    request_time = datetime.now()
    try:
        
        async with httpx.AsyncClient() as client:
            response = await client.post(tap_pay_url, json=order_data, headers=headers)
            response.raise_for_status()
            response_data = response.json()
        
        status = response_data["status"]
        order_number = response_data["rec_trade_id"]

        if status == 0:
            data = {"status": status, "order_number": order_number}
            return "OK", request_time, data
        else:
            data = {"error": True, "status": status, "message": response_data.get("msg", "Unknown error"), "order_number": order_number}
            return "API error", request_time, data
    
    except httpx.HTTPStatusError as http_err:
        error_message = http_err.response.text
        data = {"error": True, "status": http_err.response.status_code, "message": error_message}
        print(f"HTTP error occurred: {http_err}")
        return "request error", request_time, data

    except Exception as err:
        error_message = str(err)
        data = {"error": True, "status": 500, "message": error_message}
        print(f"Other error occurred: {err}")
        return "error", request_time, data

async def updateOrderStatus(db, order_id: int, status: str, order_number: str = None, paid_at: datetime = None, cancelled_at: datetime = None, completed_at: datetime = None):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalars().first()
    if order:
        order.status = status
        order.order_number = order_number
        order.paid_at = paid_at
        order.cancelled_at = cancelled_at
        order.completed_at = completed_at
        await db.commit()

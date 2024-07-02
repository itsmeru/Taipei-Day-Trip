import time
import requests
import redis
import json
from datetime import datetime
from model.getUser import getUser

def getOrders(db_pool, token, bookInfo, order_data):
    tokenData = getUser(token)
    if tokenData == "error" or tokenData is None:
            return "forbidan"
    order_redis = redis.Redis(host="localhost", port=6379, db=0)
    
    user_id = tokenData["data"]["id"]

    with db_pool.get_connection() as con:
        with con.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id FROM orders WHERE user_id = %s AND (status = 'UNPAID' OR status = 'FAILED')", (user_id,))
            existing_order = cursor.fetchone()
        
            if existing_order:
                cursor.execute("UPDATE orders SET price = %s, attraction_id = %s, attraction_name = %s, attraction_address = %s, attraction_image = %s, trip_date = %s, trip_time = %s, contact_name = %s, contact_email = %s, contact_phone = %s WHERE id = %s", (
                        bookInfo.order.price,
                        bookInfo.order.trip.attraction.id,
                        bookInfo.order.trip.attraction.name,
                        bookInfo.order.trip.attraction.address,
                        bookInfo.order.trip.attraction.image,
                        bookInfo.order.trip.date,
                        bookInfo.order.trip.time,
                        bookInfo.order.contact.name,
                        bookInfo.order.contact.email,
                        bookInfo.order.contact.phone,
                        existing_order["id"],
                ))
                con.commit()
                order_id = existing_order["id"]
            else:
                cursor.execute("INSERT INTO orders (user_id, price, attraction_id, attraction_name, attraction_address, attraction_image, trip_date, trip_time, contact_name, contact_email, contact_phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                        user_id,
                        bookInfo.order.price,
                        bookInfo.order.trip.attraction.id,
                        bookInfo.order.trip.attraction.name,
                        bookInfo.order.trip.attraction.address,
                        bookInfo.order.trip.attraction.image,
                        bookInfo.order.trip.date,
                        bookInfo.order.trip.time,
                        bookInfo.order.contact.name,
                        bookInfo.order.contact.email,
                        bookInfo.order.contact.phone,
                ))
                con.commit()
                order_id = cursor.lastrowid
                data = {
                    "user_id": user_id,
                    "price": bookInfo.order.price,
                    "attraction_id": bookInfo.order.trip.attraction.id,
                    "attraction_name": bookInfo.order.trip.attraction.name,
                    "attraction_address": bookInfo.order.trip.attraction.address,
                    "attraction_image": bookInfo.order.trip.attraction.image,
                    "trip_date": bookInfo.order.trip.date,
                    "trip_time": bookInfo.order.trip.time,
                    "contact_name": bookInfo.order.contact.name,
                    "contact_email": bookInfo.order.contact.email,
                    "contact_phone": bookInfo.order.contact.phone,
                    "status": "UNPAID"
                }
                cache_key = f"order_id:{order_id},user_id:{user_id}"
                order_redis.set(cache_key, json.dumps(data))
                order_redis.expire(cache_key, 3600)
        
            order_status, request_time, data = sendPrime(order_data, token)
            
            if order_status == "API error":
                updateOrderStatus(con, cursor, order_id, "FAILED",order_number=data["order_number"] ,cancelled_at=request_time)
                payment_result = {
                    "data": {
                        "number": data["order_number"],
                        "payment": {
                            "status": data["status"],
                            "message": "付款失敗"
                        }
                    }
                }
                return {"error":False,"payment_result":payment_result}
            elif order_status in ["request error","error"]:
                return {"error":True,"data":data}
            else:
                updateOrderStatus(con, cursor, order_id, "PAID", order_number=data["order_number"], paid_at=request_time)
                payment_result= {
                    "data": {
                        "number": data["order_number"],
                        "payment": {
                            "status": data["status"],
                            "message": "付款成功"
                        }
                    }
                }
                return {"error": False, "payment_result": payment_result}

def sendPrime(order_data, token):
    tap_pay_url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{token}",
        "x-api-key": "partner_71JD0IlN4Td4dKlAno18sKBDji9PScQ0oM0a0zkj7ZNpNxiSiG3hFzLm",
    }
    
    try:
        request_time = datetime.now()
        response = requests.post(tap_pay_url, json=order_data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        status = response_data["status"]
        order_number = response_data["rec_trade_id"]

        if status == 0:
            data = {"status": status,"order_number":order_number}
            return "OK", request_time, data
        data = {"error": True, "status": status, "message": response_data["msg"],"order_number":order_number}
        return "API error", request_time, data
    
    except requests.exceptions.HTTPError as http_err:
        error_message = http_err.response.text
        data = {"error": True, "status": http_err.response.status_code, "message": error_message}
        print(f"HTTP error occurred: {http_err}")
        return "request error", request_time, data
    
    except Exception as err:
        error_message = str(err)
        data = {"error": True, "status": 500, "message": error_message}
        print(f"Other error occurred: {err}")
        return "error", request_time, data

def updateOrderStatus(con, cursor, order_id, status, order_number=None, paid_at=None, cancelled_at=None, completed_at=None):
    cursor.execute("UPDATE orders SET status = %s, order_number = %s, paid_at = %s, cancelled_at = %s, completed_at = %s WHERE id = %s", (status, order_number, paid_at, cancelled_at, completed_at, order_id))
    con.commit()

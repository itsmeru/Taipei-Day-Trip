from fastapi import*
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from model.orders import getOrders
from view.orders import renderOrders
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
import os

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")


class Attraction(BaseModel):
    id: int
    name: str
    address: str
    image: str

class Trip(BaseModel):
    attraction: Attraction
    date: str
    time: str

class Contact(BaseModel):
    name: str
    email: str
    phone: str

class Order(BaseModel):
    price: int
    trip: Trip
    contact: Contact

class CheckInfo(BaseModel):
    prime: str
    order: Order
@router.post("/api/orders")
async def orders(bookInfo:CheckInfo,token: str= Depends(oauth2_scheme),db:AsyncSession=Depends(get_db)):
    order_data = {
        "prime": bookInfo.prime,
        "partner_key": os.getenv("PARTNER_KEY"),
        "merchant_id": os.getenv("MERCHANT_ID"),
        "details": "TapPay Test",
        "amount": bookInfo.order.price,
        "cardholder": {
            "phone_number": bookInfo.order.contact.phone,
            "name": bookInfo.order.contact.name,
            "email": bookInfo.order.contact.email,
            "zip_code": "100",
            "address": bookInfo.order.trip.attraction.address,
        },
        "remember": True,
    }

    results = await getOrders(db,token,bookInfo,order_data)
    return renderOrders(results)
   


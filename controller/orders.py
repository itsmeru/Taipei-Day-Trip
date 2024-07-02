from fastapi import*
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from model.orders import getOrders
from view.orders import renderOrders

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
async def orders(request:Request,bookInfo:CheckInfo,token: str= Depends(oauth2_scheme)):
    db_pool = request.state.db_pool.get("spot")
    order_data = {
        "prime": bookInfo.prime,
        "partner_key": "partner_71JD0IlN4Td4dKlAno18sKBDji9PScQ0oM0a0zkj7ZNpNxiSiG3hFzLm",
        "merchant_id": "tppf_itsmeru_GP_POS_3",
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

    results = await getOrders(db_pool,token,bookInfo,order_data)
    return renderOrders(results)
   


from fastapi import *
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from model.buildSchedule import getBookInfo
from model.getUser import getUser
from view.buildSchedule import renderBookInfo
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")

class Booking(BaseModel):
    attractionId: int
    date: str 
    time: str 
    price: int
@router.post("/api/booking")
async def booking(request:Request,book:Booking,token: str= Depends(oauth2_scheme),db:AsyncSession=Depends(get_db)):
    tokenData = getUser(token)
    cart={
        "attraction_id" : book.attractionId,
        "date" : book.date,
        "time" : book.time,
        "price" : book.price
    }
    redis_pool = request.state.redis_pool

    result = await getBookInfo(db,cart,tokenData,redis_pool)
    return renderBookInfo(result)

   
from fastapi import *
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from model.buildSchedule import getBookInfo
from model.getUser import getUser
from view.buildSchedule import renderBookInfo

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")

class Booking(BaseModel):
    attractionId: int
    date: str 
    time: str 
    price: int
@router.post("/api/booking")
async def booking(request:Request,book:Booking,token: str= Depends(oauth2_scheme)):
    tokenData = getUser(token)
    data={
        "token" : tokenData,
        "user_id" : tokenData["data"]["id"],
        "attraction_id" : book.attractionId,
        "date" : book.date,
        "time" : book.time,
        "price" : book.price
    }
    db_pool = request.state.db_pool.get("spot")
    result = getBookInfo(db_pool,data)
    return renderBookInfo(result)

   
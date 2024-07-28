from fastapi import *
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from model.deleteSchedule import getDeleteSchedule
from view.deleteSchedule import renderDeleteSchedule

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")


class DeleteBooking(BaseModel):
    user_id : int 
    attraction_id: int 
@router.delete("/api/booking")
async def delBooking(request:Request,booking: DeleteBooking,token: str= Depends(oauth2_scheme),db:AsyncSession=Depends(get_db)):
    redis_pool = request.state.redis_pool
    user_id = booking.user_id
    attraction_id = booking.attraction_id
    results = await getDeleteSchedule(db,user_id,attraction_id,token,redis_pool)
    return renderDeleteSchedule(results)
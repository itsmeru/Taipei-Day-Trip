from fastapi import *
from fastapi.security import OAuth2PasswordBearer
from model.getSchedule import getSchedule
from view.getSchedule import renderSchedule
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")

@router.get("/api/booking")
async def Schedule(request:Request,token: str= Depends(oauth2_scheme),db:AsyncSession=Depends(get_db)):
    redis_pool = request.state.redis_pool

    result = await getSchedule(db,token,redis_pool)
    return renderSchedule(result)

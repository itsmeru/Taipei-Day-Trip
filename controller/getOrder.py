from fastapi import *
from fastapi.security import OAuth2PasswordBearer
from model.getOrder import getOrder
from view.getOrder import renderOrder
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")

@router.get("/api/order/{orderNumber}")
async def Orders(orderNumber: str, token: str = Depends(oauth2_scheme),db:AsyncSession=Depends(get_db)):
    results = await getOrder(token,db, orderNumber)
    return renderOrder(results)

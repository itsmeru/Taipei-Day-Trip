from fastapi import *
from pydantic import BaseModel, EmailStr, Field

from model.signIn import getSignIn
from view.signIn import renderSignIn
from models import  Account
from db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()

class CheckAccount(BaseModel):
  email:EmailStr = Field(...,min_length=10, description="Invalid email format")
  password:str = Field(..., min_length=6, max_length=50, description="Password cannot be empty")



@router.put("/api/user/auth")
async def signIn(user:CheckAccount,db: AsyncSession = Depends(get_db)):
    password = user.password
    email = user.email
    results = await getSignIn(db, email, password,Account)
    return renderSignIn(results)
   
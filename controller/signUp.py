from fastapi import *
from pydantic import BaseModel, EmailStr, Field
from model.hashpwd import hash_password
from model.signUp import getSignUp
from view.signUp import renderSignUp
from models import Account
from db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

class CheckAccount(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Name cannot be empty")
    email: EmailStr = Field(..., description="Invalid email format")
    password: str = Field(..., min_length=6, max_length=50, description="Password cannot be empty")


@router.post("/api/user")
async def signUp(user:CheckAccount,db: AsyncSession= Depends(get_db)):
  try:
    name = user.name
    email = user.email
    password = hash_password(user.password)
  except:
    name = user["name"]
    email = user["email"]
    password = hash_password(user["password"])

  results = await getSignUp(db, name, email, password,Account)
  return renderSignUp(results)
  
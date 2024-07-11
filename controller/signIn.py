from fastapi import *
from pydantic import BaseModel, EmailStr, Field

from model.signIn import getSignIn
from view.signIn import renderSignIn
router = APIRouter()

class CheckAccount(BaseModel):
  email:EmailStr = Field(...,min_length=10, description="Invalid email format")
  password:str = Field(..., min_length=6, max_length=50, description="Password cannot be empty")


@router.put("/api/user/auth")
async def signIn(request:Request,user:CheckAccount):
    password = user["password"]
    email = user["email"]
    db_pool = request.state.db_pool.get("spot")
    results = getSignIn(db_pool, email, password)
    return renderSignIn(results)
   
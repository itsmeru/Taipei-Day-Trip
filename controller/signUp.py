from fastapi import *
from pydantic import BaseModel, EmailStr, Field
from model.hashpwd import hash_password
from model.signUp import getSignUp
from view.signUp import renderSignUp
router = APIRouter()

class CheckAccount(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Name cannot be empty")
    email: EmailStr = Field(..., description="Invalid email format")
    password: str = Field(..., min_length=6, max_length=50, description="Password cannot be empty")


@router.post("/api/user")
async def signUp(request:Request,user:CheckAccount):
  name = user.name
  email = user.email
  password = hash_password(user.password)

  db_pool = request.state.db_pool.get("spot")
  results = getSignUp(db_pool, name, email, password)
  return renderSignUp(results)
  
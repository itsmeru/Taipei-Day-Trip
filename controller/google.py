from fastapi import *
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
from model.signIn import getSignIn
from controller.signUp import signUp
from models import Account

from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db 
from fastapi.responses import JSONResponse
import os

router = APIRouter()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
class Token(BaseModel):
    id_token: str

@router.post("/auth/google")
async def google_auth(token: Token,db: AsyncSession = Depends(get_db)):
    try:
        clientId = CLIENT_ID
        idInfo = id_token.verify_oauth2_token(token.id_token, requests.Request(), clientId)
        email = idInfo["email"]
        name = idInfo["name"]
        password = idInfo["sub"]
        singUp_data = {"name":name,"email":email,"password":password}
        singnUpResult = await signUp(user=singUp_data,db=db)
        signIn_response = await getSignIn(db,email,password,Account)
        data = {"data":{"id": signIn_response["id"], "name": name, "email": email},"token":signIn_response["token"]}
        return data
    except ValueError:
        data = {"data":None}
        return  JSONResponse(status_code=400, content = data,media_type="application/json")


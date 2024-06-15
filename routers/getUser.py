from fastapi import *
from fastapi.responses import JSONResponse
import os
import jwt

router = APIRouter()

jwt_secret =os.environ.get("JWT_SECRECT")
algo=os.environ.get("ALGORITHM")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=[algo])
        id = payload.get("id")
        return id
    except jwt.PyJWTError as e:
        return None
    
async def get_current_user(request: Request):
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        data = {"message":"Bearer token not provided"}
        return JSONResponse(status_code=401,content=data,media_type="application/json")
     
    token = authorization.split(" ")[1]
    id = verify_token(token)
    if id is None or request.session.get("email") is None :
        data = {"data": None}
        return JSONResponse(content=data,media_type="application/json")
    else:
        data = {"data":{"id": id, "name": request.session["name"], "email": request.session["email"]}}
        return JSONResponse(content=data,media_type="application/json")

@router.get("/api/user/auth")
async def getUser(request:Request,current_user: dict = Depends(get_current_user)):
    return current_user
    
from fastapi import *
import os
from model.getUser import getUser
from view.getUser import renderUser
router = APIRouter()

jwt_secret =os.environ.get("JWT_SECRECT")
algo=os.environ.get("ALGORITHM")

    
async def get_current_user(request:Request):
    authorization = request.headers.get("Authorization")
    return getUser(authorization, jwt_secret, algo)

@router.get("/api/user/auth")
async def getUser(request:Request):
    results = get_current_user()
    return renderUser(results)
    
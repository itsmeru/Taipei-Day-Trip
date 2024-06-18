from fastapi import *
import os
from model.getUser import getUser
from view.getUser import renderUser
router = APIRouter()

jwt_secret = os.environ.get("JWT_SECRET")
algo=os.environ.get("ALGORITHM")

    
@router.get("/api/user/auth")
async def getUsers(request:Request):
    authorization = request.headers.get("Authorization")
    results = getUser(authorization, jwt_secret, algo)
    return renderUser(results)
    
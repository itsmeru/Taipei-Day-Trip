from fastapi import *
from fastapi.security import OAuth2PasswordBearer
from model.getUser import getUser
from view.getUser import renderUser
router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")
    
@router.get("/api/user/auth")
async def getUsers(token: str= Depends(oauth2_scheme)):
    results = getUser(token)
    return renderUser(results)
    
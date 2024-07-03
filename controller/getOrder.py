from fastapi import *
from fastapi.security import OAuth2PasswordBearer
from model.getOrder import getOrder
from view.getOrder import renderOrder

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")

@router.get("/api/order/{orderNumber}")
def Orders(request: Request, orderNumber: str, token: str = Depends(oauth2_scheme)):
    db_pool = request.state.db_pool.get("spot")
    results = getOrder(token,db_pool, orderNumber)
    return renderOrder(results)

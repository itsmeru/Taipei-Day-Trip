from fastapi import *
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()

class DeleteBooking(BaseModel):
    user_id : int = 1
    attraction_id: int = 1
@router.delete("/api/booking")
async def delBooking(request:Request,booking: DeleteBooking):
    try:
        if request.session.get("email") is None or request.session.get("token") is  None:
            data = {"error":True,"message":"未登入系統，拒絕存取"}
            return JSONResponse(status_code=403,content=data,media_type="application/json")
        db_pool = request.state.db_pool.get("spot")
        attraction_id = booking.attraction_id
        user_id = booking.user_id
        with db_pool.get_connection() as con:
            with con.cursor() as cursour:
                cursour.execute("delete from schedule where attraction = %s and user_id = %s",(attraction_id,user_id))
                con.commit()
            data = {"ok":True}
            return JSONResponse(content=data,media_type="application/json")
    except Exception as e:
        data = {"error":True,"message":"未登入系統，拒絕存取"}
        return JSONResponse(status_code=403,content=data,media_type="application/json")
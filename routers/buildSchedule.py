from fastapi import *
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()

class Booking(BaseModel):
    user_id :int 
    attraction_id: int
    date: str 
    time: str 
    price: int 
@router.post("/api/booking")
async def booking(request:Request,book:Booking):
    user_id = book.user_id
    attraction_id = book.attraction_id
    date = book.date
    time = book.time
    price = book.price
    db_pool = request.state.db_pool.get("spot")
    try:
        if request.session.get("email") is None or request.session.get("token") is  None:
            data = {"error":True,"message":"未登入系統，拒絕存取"}
            return JSONResponse(status_code=403,content=data,media_type="application/json")

        with db_pool.get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("insert into schedule(user_id,attraction_id,date,time,price)values(%s,%s,%s,%s,%s)",(user_id,attraction_id,date,time,price))
                con.commit()
        data = {"ok":True}
        return JSONResponse(content=data,media_type="application/json")
    except HTTPException as http_exc:
        return JSONResponse(status_code=http_exc.status_code, content={"error": True, "message": http_exc.detail})
    except Exception as e:
        print(e)
        data = {"error":True,"message":"伺服器內部錯誤"}
        return JSONResponse(status_code=500,content=data,media_type="application/json")
   
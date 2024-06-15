from fastapi import *
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from routers.hashpwd import hash_password
router = APIRouter()

class CheckAccount(BaseModel):
  name:str
  email:str
  password:str


@router.post("/api/user")
async def signUp(request:Request,user:CheckAccount):
  name = user.name
  email = user.email
  password = hash_password(user.password)

  db_pool = request.state.db_pool.get("spot")
  try:
    with db_pool.get_connection() as con:
        with con.cursor(dictionary = True) as cursor:
            cursor.execute("select id from account where email = %s",(email,))
            existing_user = cursor.fetchone()
            if existing_user : 
                data = {"error": True, "message": "註冊失敗，重複的 Email"}
                return JSONResponse(status_code=400, content=data, media_type="application/json")
            cursor.execute("insert into account(name,email,password) values(%s,%s,%s)",(name,email,password))
            con.commit()
            data = {"ok": True}
            return JSONResponse(content=data, media_type="application/json")
  except Exception as e:
        print(f"Unhandled exception: {e}")
        data = {"error": True, "message": "伺服器內部錯誤"}
        return JSONResponse(status_code=500, content=data, media_type="application/json")
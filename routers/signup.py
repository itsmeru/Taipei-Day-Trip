from fastapi import *
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.responses import JSONResponse

router = APIRouter()

class checkAccount(BaseModel):
  name:str
  email:str
  password:str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/api/user")
async def signUp(request:Request,user:checkAccount):
  name = user.name
  email = user.email
  password = hash_password(user.password)

  db_pool = request.state.db_pool.get("member")
  try:
    with db_pool.get_connection() as con:
        with con.cursor(dictionary = True) as cursour:
            cursour.execute("select id from account where email = %s",(email,))
            existing_user = cursour.fetchone()
            if existing_user : 
                data = {"error": True, "message": "註冊失敗，重複的 Email"}
                return JSONResponse(status_code=400, content=data, media_type="application/json")
            cursour.execute("insert into account(name,email,password) values(%s,%s,%s)",(name,email,password))
            con.commit()
            data = {"ok": True}
            return JSONResponse(content=data, media_type="application/json")
  except Exception as e:
        print(f"Unhandled exception: {e}")
        data = {"error": True, "message": "伺服器內部錯誤"}
        return JSONResponse(status_code=500, content=data, media_type="application/json")
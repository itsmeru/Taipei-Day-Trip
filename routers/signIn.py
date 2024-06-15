from datetime import datetime, timedelta
from fastapi import *
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import jwt
from routers.hashpwd import verify_password
import os
router = APIRouter()

class CheckAccount(BaseModel):
  email:str
  password:str
@router.put("/api/user/auth")
async def signIn(request:Request,user:CheckAccount):
    email = user.email
    password = user.password
    db_pool = request.state.db_pool.get("spot")
    try:
        with db_pool.get_connection() as con:
            with con.cursor(dictionary = True) as cursor:
                cursor.execute("select * from account where email = %s",(email,))
                existing_user = cursor.fetchone()
                if existing_user:
                    hash_pwd = existing_user["password"]
                    if verify_password(password,hash_pwd):
                        token_payload = {
                            "id": existing_user["id"],
                            "exp": datetime.utcnow() + timedelta(days=7)  
                        }
                        header = {
                            "typ": "JWT",
                            "alg": "HS256"
                        }
                        jwt_secret = os.environ.get("JWT_SECRET")
                        algo = os.environ.get("ALGORITHM")
                        token = jwt.encode(token_payload, jwt_secret, algorithm=algo,headers=header)
                        request.session["id"] = existing_user["id"]
                        request.session["name"] = existing_user["name"]
                        request.session["email"] = existing_user["email"]
                        request.session["token"] = token

                        data = {"token": token}
                        return JSONResponse(content=data,media_type="application/json")
                    data = {"error": True,"message": "密碼驗證失敗"}
                    return JSONResponse(status_code=400,content = data,media_type="application/json")   
                data = {"error": True, "message": "用戶不存在"}
                return JSONResponse(status_code=404, content=data, media_type="application/json")

    except Exception as e:
        print(f"Unhandled exception: {e}")
        data = {"error": True, "message": "伺服器內部錯誤"}
        return JSONResponse(status_code=500, content=data, media_type="application/json")
   
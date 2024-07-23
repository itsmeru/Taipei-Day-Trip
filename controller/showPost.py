from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv


load_dotenv()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")

@router.get("/api/showPost")
async def showFile(request:Request,token: str= Depends(oauth2_scheme)):
    db_pool = request.state.db_pool.get("board")
    data = []
    try:
        with db_pool.get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("select * from comments order by timestamp DESC")
                results = cursor.fetchall()
                if results:
                    for result in results:
                        data.append({"text":result["content"],"imageUrl":result["image_url"]})
                else:
                    data.append({"text":None})
            return JSONResponse(content=data)
            
    except Exception as e:
            print(e)
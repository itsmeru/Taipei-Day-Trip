from fastapi import APIRouter, Request,FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
router = APIRouter()
app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    data = {"error": True, "message": "輸入錯誤"}
    return JSONResponse(status_code=422, content=data, media_type="application/json")
@router.get("/api/attraction/{attractionId}")
async def attraction_spot(request: Request, attractionId: int):
    try:
        db_pool = request.state.db_pool.get("spot")
        with db_pool.get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM spots WHERE id = %s", (attractionId,))
                spots_data = cursor.fetchone()
                if not spots_data:
                    data = {"error": True, "message": "找不到此景點"}
                    return JSONResponse(status_code=404, content=data, media_type="application/json")
                cursor.execute("SELECT images FROM spot_imgs WHERE img_id = %s", (attractionId,))
                img_urls = [row["images"] for row in cursor.fetchall()]
                spots_data["images"] = img_urls
                data = {"data":spots_data}
                return JSONResponse(content=data, media_type="application/json")
    except Exception as e:
        print(f"Unhandled exception: {e}")
        data = {"error": True, "message": "伺服器內部錯誤"}
        return JSONResponse(status_code=500, content=data, media_type="application/json")

app.include_router(router)

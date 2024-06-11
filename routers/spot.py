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
        db_pool = request.state.db_pool
        with db_pool.get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM spots WHERE id = %s", (attractionId,))
                results = cursor.fetchone()
                if not results:
                    data = {"error": True, "message": "找不到此景點"}
                    return JSONResponse(status_code=404, content=data, media_type="application/json")

                cursor.execute("SELECT spots.*, imgs.images FROM spots JOIN (SELECT img_id, GROUP_CONCAT(img_url) AS images FROM spot_imgs GROUP BY img_id) AS imgs ON spots.id = imgs.img_id WHERE spots.id = %s",(attractionId,))
                datas = cursor.fetchall()
                result = datas[0]
                image_urls = result["images"].split(",") if result["images"] else []
                result["images"] = image_urls 
                data = {"data": result}
                return JSONResponse(content=data, media_type="application/json")
    except Exception as e:
        print(f"Unhandled exception: {e}")
        data = {"error": True, "message": "伺服器內部錯誤"}
        return JSONResponse(status_code=500, content=data, media_type="application/json")

app.include_router(router)

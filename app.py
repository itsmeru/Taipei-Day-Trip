from fastapi import *
from pydantic import BaseModel
from fastapi.responses import FileResponse
import mysql.connector.pooling
from fastapi.responses import JSONResponse
app=FastAPI()
dbconfig = {
    "database": "spot",
    "user": "root",
    "password": "betty520"
}
cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)
@app.middleware("http")
async def attach_db_connection(request: Request, call_next):
   
    request.state.db_pool = cnxpool
    response = await call_next(request)
    return response
# Static Pages (Never Modify Code in this Block)
class attraction_type(BaseModel):
	page: int = Query(0, description="要取得的分頁，每頁 12 筆資料")
	keyword: str = Query("", description="關鍵字")
@app.get("/", include_in_schema=False)
async def get_data(request:Request):
	# db_pool = request.state.db_pool
	# cnx = db_pool.get_connection()
	# with cnx.cursor() as cursor:
	# 	cursor.execute("SELECT * FROM spots")
	# 	data = cursor.fetchall()
	return {"data": True}

@app.get("/api/attractions")
async def attractions(request: Request, page: int = Query(0, description="要取得的分頁，每頁 12 筆資料"), keyword: str = Query("", description="用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做篩選")):
    
    items_per_page = 12
    start_index = page * items_per_page
    db_pool = request.state.db_pool
	
    with db_pool.get_connection() as con:
        with con.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM spots WHERE description LIKE %s LIMIT %s,%s", ('%' + keyword + '%', start_index, items_per_page))
            results = cursor.fetchall()
            if not results:
                data = {"error": True, "message": "找不到對應的資料"}
                return JSONResponse(content=data)
            
            cursor.execute("SELECT spots.id, spot_imgs.img_url FROM spots JOIN spot_imgs ON spots.id = spot_imgs.img_id GROUP BY spots.id, spot_imgs.img_url")
            datas =  cursor.fetchall()
    attractions = []
    for result in results:
        image_urls = [data["img_url"] for data in datas if data["id"] == result["id"]]
        attraction = {
            "id": result["id"],
            "name": result["name"],
            "category": result["category"],
            "description": result["description"],
            "address": result["address"],
            "transport": result["transpot"],
            "mrt": result["MRT"],
            "lat": result["lat"],
            "lng": result["lng"],
            "images": image_urls
        }
        attractions.append(attraction)
    next_page = page + 1
    data = {"nextPage": next_page, "data": attractions}
    return JSONResponse(content=data)


@app.get("/api/attraction/{attractionId}")
async def attraction_spot(request: Request, attractionId: int):
    try:
        db_pool = request.state.db_pool
        with db_pool.get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM spots WHERE id = %s", (attractionId,))
                result = cursor.fetchone()
                if not result:
                    data = {"error": True, "message": "找不到此景點"}
                    return JSONResponse(content=data)
                
                
                cursor.execute("SELECT spot_imgs.id, spot_imgs.img_url FROM spots JOIN spot_imgs ON spots.id = spot_imgs.img_id WHERE spots.id = %s", (attractionId,))
                datas = cursor.fetchall()
                
                image_urls = [data["img_url"] for data in datas]
                
                attraction = {
                    "id": result["id"],
                    "name": result["name"],
                    "category": result["category"],
                    "description": result["description"],
                    "address": result["address"],
                    "transport": result["transpot"],
                    "mrt": result["MRT"],
                    "lat": result["lat"],
                    "lng": result["lng"],
                    "images": image_urls
                }
                data = {"data": attraction}  
                return JSONResponse(content=data)
    except :
        data = {"error": True, "message": "伺服器內部錯誤"}
        return JSONResponse(content=data)

@app.get("/api/mrts")
async def get_mrt(request: Request):
    try:
        db_pool = request.state.db_pool
        with db_pool.get_connection() as con:
            with con.cursor() as cursor:
                cursor.execute("SELECT MRT FROM spots")
                results = cursor.fetchall()
            mrt_data = []
            for result in results:
                mrt_data.append(result[0])
            data = {"data":mrt_data}
            return JSONResponse(content=data)
    except:
        data = {"error": True,"message": "伺服器內部錯誤"}
        return JSONResponse(content=data)
		
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")
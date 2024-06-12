from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/api/attractions")
async def attractions(request: Request, page: int = Query(0, description="要取得的分頁，每頁 12 筆資料"), keyword: str = Query("", description="用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做篩選")):
    items_per_page = 12
    start_index = page * items_per_page
    db_pool = request.state.db_pool.get("spot")
    
    with db_pool.get_connection() as con:
        with con.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM spots WHERE MRT = %s OR name LIKE %s", (keyword, '%' + keyword + '%'))
            results = cursor.fetchall()
            total_num = len(results)
            total_page = total_num / 12
            cursor.execute("SELECT spots.*, imgs.images FROM spots JOIN (SELECT img_id, GROUP_CONCAT(img_url) AS images FROM spot_imgs GROUP BY img_id) AS imgs ON spots.id = imgs.img_id WHERE (spots.MRT = %s OR spots.name LIKE %s) LIMIT %s,%s", (keyword, '%' + keyword + '%', start_index, items_per_page))
            results = cursor.fetchall()
            if not results:
                data = {"error": True, "message": "找不到對應的資料"}
                return JSONResponse(status_code=404, content=data, media_type="application/json")
    for result in results:
        image_urls = result["images"].split(",") if result["images"] else []
        result ["images"] = image_urls
    next_page = page + 1 if page + 1 < total_page else None
    data = {"nextPage": next_page, "data": results}
    return JSONResponse(content=data, media_type="application/json")

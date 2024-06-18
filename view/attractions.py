from fastapi.responses import JSONResponse
def renderAttractions(results, page, total_page):
    if results is None:
        data = {"error": True, "message": "找不到對應的資料"}
        return JSONResponse(status_code=404,content=data)
    elif results == "error":
        data = {"error": True, "message": "伺服器內部錯誤"}
        return JSONResponse(status_code=500, content=data, media_type="application/json")
    else:
        next_page = page + 1 if page + 1 < total_page else None
        data = {"nextPage": next_page, "data": results}
        return JSONResponse(content=data, media_type="application/json")

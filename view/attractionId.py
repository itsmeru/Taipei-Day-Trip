from fastapi.responses import JSONResponse


def renderAttractionId(results):
    if results is None:
        data = {"error": True, "message": "找不到此景點"}
        return JSONResponse(status_code=404, content=data, media_type="application/json")
    elif results == "error":
        data = {"error": True, "message": "伺服器內部錯誤"}
        return JSONResponse(status_code=500, content=data, media_type="application/json")
    else:
        return JSONResponse(content=results, media_type="application/json")


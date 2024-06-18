from fastapi.responses import JSONResponse

def renderMrts(results):
    if results == "error":
        data = {"error": True, "message": "伺服器內部錯誤"}
        return JSONResponse(status_code=500, content=data, media_type="application/json")
    return JSONResponse(content=results, media_type="application/json")

    
from fastapi.responses import JSONResponse

def renderDeleteSchedule(results):
    if results == "forbidan":
        data = {"error":True,"message":"未登入系統，拒絕存取"}
        return JSONResponse(status_code=403,content=data,media_type="application/json")
    elif results == "error":
        data = {"error": True, "message": "伺服器內部錯誤"}
        return JSONResponse(status_code=500,content=data,media_type="application/json")
    else:
        return JSONResponse(content=results,media_type="application/json")

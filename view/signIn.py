from fastapi.responses import JSONResponse


def renderSignIn(results):
    if results == "pwdfail":
        data = {"error": True,"message": "電子郵件或密碼錯誤"}
        return JSONResponse(status_code=400,content = data,media_type="application/json")
    elif results == "userfail":
        data = {"error": True, "message": "用戶不存在"}
        return JSONResponse(status_code=404, content=data, media_type="application/json")
    elif results == "error":
        data = {"error": True, "message": "伺服器內部錯誤"}
        return JSONResponse(status_code=500, content=data, media_type="application/json")
    else:
        return JSONResponse(content=results,media_type="application/json")


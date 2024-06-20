from fastapi.responses import JSONResponse


def renderSignUp(results):
    if results == "mailrepeat":
        data = {"error": True, "message": "註冊失敗，重複的 Email"}
        return JSONResponse(status_code=400, content=data, media_type="application/json")
    elif results == "error":
        data = {"error": True, "message": "伺服器內部錯誤"}
        return JSONResponse(status_code=500, content=data, media_type="application/json")
    else:
        return JSONResponse(content=results, media_type="application/json")

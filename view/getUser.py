from fastapi.responses import JSONResponse


def renderUser(results):
    if results is None:
        data = {"data": None}
        return JSONResponse(content=data,media_type="application/json")
    elif results == "provided":
        data = {"message":"Bearer token not provided"}
        return JSONResponse(status_code=401,content=data,media_type="application/json")
    else:
        return JSONResponse(content=data,media_type="application/json")

    
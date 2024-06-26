from fastapi.responses import JSONResponse


def renderUser(results):
        if results == "error":
                data = {"error": "Token has expired"}
                return JSONResponse(status_code=404,content = data,media_type="application/json")
        elif results == "sessionError":
                data = {"error": "Session Error"}
                return JSONResponse(status_code=404,content = data,media_type="application/json")
        return JSONResponse(content=results,media_type="application/json")

    
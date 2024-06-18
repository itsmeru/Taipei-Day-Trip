from fastapi.responses import JSONResponse


def renderUser(results):
        return JSONResponse(content=results,media_type="application/json")

    
from fastapi.responses import JSONResponse

def renderOrders(results):
    print(results)
    if results == "forbidan":
        data = {"error":True,"message":"未登入系統，拒絕存取"}
        return JSONResponse(status_code=403,content=data,media_type="application/json")
    elif results["error"]:
        data = {"error": True, "message": results["message"]}
        return JSONResponse(status_code=400, content=data,media_type="application/json")
    else:
        return JSONResponse(content=results["payment_result"],media_type="application/json")
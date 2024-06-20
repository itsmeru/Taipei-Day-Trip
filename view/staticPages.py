from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/", include_in_schema=False)
async def index():
    return FileResponse("./static/index.html", media_type="text/html")

@router.get("/attraction/{id}", include_in_schema=False)
async def attraction(id: int):
    return FileResponse("./static/attraction.html", media_type="text/html")

@router.get("/booking", include_in_schema=False)
async def booking():
    return FileResponse("./static/booking.html", media_type="text/html")

@router.get("/thankyou", include_in_schema=False)
async def thankyou():
    return FileResponse("./static/thankyou.html", media_type="text/html")

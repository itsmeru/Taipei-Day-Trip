from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from routers import attractions, mrts, static_pages, spot
from database import create_db_pool

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

db_pool = create_db_pool()

@app.middleware("http")
async def attach_db_connection(request, call_next):
    request.state.db_pool = db_pool
    response = await call_next(request)
    return response


app.include_router(attractions.router)
app.include_router(mrts.router)
app.include_router(static_pages.router)
app.include_router(spot.router)



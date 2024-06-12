from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from routers import attractions, mrts, static_pages, spot, signup
from database import create_db_pool
# from starlette_session import SessionMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# app.add_middleware(
#     SessionMiddleware,
#     secret_key="ruruisthebest",
#     max_age=None,
#     cookie_name="session_data",
#     # cookie_secure=True,
#     # cookie_httponly=True  
# )


db_pool ={
    "spot":create_db_pool("spot"),
    # "member":create_db_pool("member"),
}
@app.middleware("http")
async def attach_db_connection(request, call_next):
    request.state.db_pool = db_pool
    response = await call_next(request)
    return response


app.include_router(attractions.router)
app.include_router(mrts.router)
app.include_router(static_pages.router)
app.include_router(spot.router)
app.include_router(signup.router)




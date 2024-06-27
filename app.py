from fastapi import *
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from controller import attractionId, attractions, buildSchedule, getUser, mrts, signIn, signUp, getSchedule,deleteSchedule,tappay
from starlette_session import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from exceptions import *
from view import staticPages


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.middleware("http")(db_connection)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(
#     SessionMiddleware,
#     secret_key="ruruisthebest",
#     max_age=3600,
#     cookie_name="session_data",    
# )


app.include_router(attractions.router)
app.include_router(mrts.router)
app.include_router(staticPages.router)
app.include_router(attractionId.router)
app.include_router(signUp.router)
app.include_router(signIn.router)
app.include_router(getUser.router)
app.include_router(buildSchedule.router)
app.include_router(getSchedule.router)
app.include_router(deleteSchedule.router)
app.include_router(tappay.router)








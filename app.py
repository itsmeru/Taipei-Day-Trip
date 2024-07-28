from fastapi import *
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from controller import attractionId, attractions, buildSchedule, getUser, mrts, orders, signIn, signUp, getSchedule,deleteSchedule,getOrder,google,upload,showPost
import redis

from exceptions import *
from view import staticPages
from dotenv import load_dotenv

load_dotenv()



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_redis_connection():
    return redis.StrictRedis(host="redis", port=6379, db=0)

redis_pool = get_redis_connection()


async def redis_connection(request: Request, call_next):
    request.state.redis_pool = redis_pool
    response = await call_next(request)
    return response

app.middleware("http")(redis_connection)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)


app.include_router(upload.router)
app.include_router(showPost.router)
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
app.include_router(orders.router)
app.include_router(getOrder.router)
app.include_router(google.router)










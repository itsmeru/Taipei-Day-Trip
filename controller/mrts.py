from fastapi import APIRouter, Request
from model.mrts import getMrt
from view.mrts import renderMrts

router = APIRouter()

@router.get("/api/mrts")
async def get_mrt(request: Request):
    db_pool = request.state.db_pool.get("spot")
    results = getMrt(db_pool)
    return renderMrts(results)
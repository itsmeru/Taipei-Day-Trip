from fastapi import APIRouter, Request
from model.attractionId import getAttractionId
from view.attractionId import renderAttractionId

router = APIRouter()


@router.get("/api/attraction/{attractionId}")
async def attraction_spot(request: Request, attractionId: int):
        db_pool = request.state.db_pool.get("spot")
        redis_pool = request.state.redis_pool
        results = getAttractionId(db_pool, attractionId,redis_pool)
        return renderAttractionId(results)


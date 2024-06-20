from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from model.attractionId import getAttractionId
from view.attractionId import renderAttractionId
router = APIRouter()


@router.get("/api/attraction/{attractionId}")
async def attraction_spot(request: Request, attractionId: int):
        db_pool = request.state.db_pool.get("spot")
        results = getAttractionId(db_pool, attractionId)
        return renderAttractionId(results)


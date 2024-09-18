from fastapi import APIRouter, Depends, Request
from model.attractionId import getAttractionId
from view.attractionId import renderAttractionId
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db

router = APIRouter()


@router.get("/api/attraction/{attractionId}")
async def attraction_spot(request: Request, attractionId: int,db: AsyncSession = Depends(get_db)):
        redis_pool = request.state.redis_pool
        results = await getAttractionId(db, attractionId,redis_pool)
        return renderAttractionId(results)


from fastapi import APIRouter, Depends
from model.mrts import getMrt
from view.mrts import renderMrts
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db

router = APIRouter()

@router.get("/api/mrts")
async def get_mrt(db:AsyncSession = Depends(get_db)):
    results = await getMrt(db)
    return renderMrts(results)
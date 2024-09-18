from fastapi import *
from model.attractions import getAttractions
from view.attractions import renderAttractions
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
router = APIRouter()

@router.get("/api/attractions")
async def attractions(request: Request, page: int = Query(0, description="要取得的分頁，每頁 12 筆資料"), keyword: str = Query("", description="用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做篩選"),db :AsyncSession = Depends(get_db)):
    items_per_page = 12
    start_index = page * items_per_page
    redis_pool = request.state.redis_pool

    data = await getAttractions(db,start_index, items_per_page, keyword,redis_pool)
    results = data["results"]
    total_page = data["total_page"]
    return renderAttractions(results, page, total_page)
   
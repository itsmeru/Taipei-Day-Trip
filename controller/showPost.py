from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession



from models import Comment  
from db import get_db  
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")

@router.get("/api/showPost")
async def showFile(token: str= Depends(oauth2_scheme),db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Comment).order_by(Comment.timestamp.desc())
        results = await db.execute(stmt)
        comments = results.scalars().all()
        data = [{"text": result.content, "imageUrl": result.image_url} for result in comments]
        return JSONResponse(content=data)
    except Exception as e:
        print(e)
        return JSONResponse(content={"success": False, "message": str(e)}, status_code=500)
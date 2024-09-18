import mimetypes
from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import boto3
import os
from pydantic import BaseModel
from boto3.s3.transfer import TransferConfig
import uuid

from model.getUser import getUser
from models import Comment
from db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
    region_name=os.getenv("BUCKET_REGION")
)
bucket_name = os.getenv("BUCKET_NAME")

class checkFile(BaseModel):
    text: str  
    picture: UploadFile


@router.post("/api/upload")
async def upload_file(text: str = Form(...),picture: UploadFile = File(...),token: str= Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    tokenData = getUser(token)
    user_id = tokenData["data"]["id"]
    user_name = tokenData["data"]["name"]

    try:
        mime_type, _ = mimetypes.guess_type(picture.filename)
        if mime_type is None:
            mime_type = "application/octet-stream"
        config = TransferConfig(
            multipart_threshold=1024 * 50,  # 50 MB
            multipart_chunksize=1024 * 50   # 50 MB
        )
        unique_filename = f"{uuid.uuid4()}{os.path.splitext(picture.filename)[1]}"
        s3_key = f"images/{unique_filename}"
        s3_client.upload_fileobj(picture.file, bucket_name, s3_key, ExtraArgs={"ContentType": mime_type}, Config=config)
        image_url = f"{os.getenv('CLOUDFRONT_DOMAIN')}/{s3_key}"

        new_comment = Comment(
            user_id=user_id,
            user_name=user_name,
            content=text,
            image_url=image_url
        )
        db.add(new_comment)
        await db.commit()
        
        return JSONResponse(content={"success": True})
    except Exception as e:
        return JSONResponse(content={"success": False, "message": str(e)}, status_code=500)
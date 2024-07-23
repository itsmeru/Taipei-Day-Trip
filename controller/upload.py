import mimetypes
from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import boto3
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from model.getUser import getUser
from boto3.s3.transfer import TransferConfig

load_dotenv()
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
async def upload_file(request:Request,text: str = Form(...),picture: UploadFile = File(...),token: str= Depends(oauth2_scheme)):
    tokenData = getUser(token)
    user_id = tokenData["data"]["id"]
    user_name = tokenData["data"]["name"]
    db_pool = request.state.db_pool.get("board")
    try:
        mime_type, _ = mimetypes.guess_type(picture.filename)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        config = TransferConfig(
            multipart_threshold=1024 * 50,  # 50 MB
            multipart_chunksize=1024 * 50   # 50 MB
        )
        s3_key = f"images/{picture.filename}"
        s3_client.upload_fileobj(picture.file, bucket_name, s3_key,ExtraArgs={'ContentType': mime_type}, Config=config)
        image_url = f"{os.getenv("CLOUDFRONT_DOMAIN")}/{s3_key}"

        try:
            with db_pool.get_connection() as con:
                with con.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO comments (user_id, user_name, content, image_url) VALUES (%s, %s, %s, %s)", 
                        (user_id, user_name, text, image_url)
                    )
                    con.commit()
            return JSONResponse(content={"success": True})
        except Exception as e:
            print(e)
    except Exception as e:
        return JSONResponse(content={"success": False, "message": str(e)}, status_code=500)
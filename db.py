from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

import os
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
DATABASE_URL = f"mysql+aiomysql://{os.getenv('RDS_USER')}:{os.getenv('RDS_PASSWORD')}@{os.getenv('RDS_HOST')}:{os.getenv('RDS_PORT')}/{os.getenv('RDS_TPE')}"
# DATABASE_URL = f"mysql+aiomysql://{os.getenv('RDS_USER')}:{os.getenv('RDS_PASSWORD')}@127.0.0.1:3307/{os.getenv('RDS_TPE')}"

# DATABASE_URL = f"mysql+aiomysql://root:betty520@localhost:3306/spot"



engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800
)

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

async def get_db():
    async with async_session() as session:
        yield session
        await session.close()
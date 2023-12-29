from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine

from settings import settings

BASE_DIR = Path(__file__).parent.parent

async_engine = create_async_engine(f"{settings.db_urls.async_db_url}///{BASE_DIR}/rzddate.db", echo=True)












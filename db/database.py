from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from settings import settings

BASE_DIR = Path(__file__).parent.parent

async_engine = create_async_engine(f"{settings.db_urls.async_db_url}{BASE_DIR}/rzddate.db", echo=False)

sync_engine = create_engine(f"{settings.db_urls.sync_db_url}{BASE_DIR}/rzddate.db", echo=False,
)

async_session_factory = async_sessionmaker(async_engine)
session_factory = sessionmaker(sync_engine)












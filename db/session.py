from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .config import sqlite_config

SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{sqlite_config.path}/{sqlite_config.db_name}.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL,
                            echo=True,
                            execution_options={"isolation_level": "AUTOCOMMIT"})

async_session = sessionmaker(engine, class_=AsyncSession)


async def get_db() -> AsyncGenerator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()

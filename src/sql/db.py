import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config import DB_USER, DB_HOST, DB_PORT, DB_NAME, DB_PASS

DB_URL =f"sqlite+aiosqlite:///school.db"

engine = create_async_engine(DB_URL)

async def ss_maiker() -> AsyncSession:
    session = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with session.begin() as session:
        return session

def get_session() -> AsyncSession:
    session = asyncio.run(ss_maiker())
    return session


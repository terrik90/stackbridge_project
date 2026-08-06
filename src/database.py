from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg(),
    echo=True,
    pool_size=5,
    max_overflow=10,
)


async_session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=False)


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker

from core.config.loader import envs


class DataBase:
    def __init__(self):
        self._engine: AsyncEngine = create_async_engine(
            url=envs.postgres_url,
            echo=False,
        )

        self._session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @property
    def async_engine(self) -> AsyncEngine:
        return self._engine

    @property
    def async_session(self) -> async_sessionmaker[AsyncSession]:
        return self._session

    # Create all tables
    async def create_table(
            self,
            metadata: MetaData,
    ) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(metadata.create_all)

    # Delete all tables
    async def delete_table(
            self,
            metadata: MetaData,
    ) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)


database = DataBase()

from sqlalchemy.orm import DeclarativeBase

from core.db.manager import BaseManager, Table


class BaseModel(DeclarativeBase):
    __abstract__ = True

    @classmethod
    async def create(cls, **kwargs) -> Table:
        queryset = BaseManager(cls)

        return await queryset.create(**kwargs)

    @classmethod
    async def update(cls, **kwargs) -> list[Table]:
        queryset = BaseManager(cls)

        return await queryset.update(**kwargs)

    @classmethod
    async def delete(cls) -> None:
        queryset = BaseManager(cls)

        return await queryset.delete()

    @classmethod
    def filter(cls, **kwargs) -> "BaseManager":
        queryset = BaseManager(cls)

        return queryset.filter(**kwargs)

    @classmethod
    def order_by(cls, *args) -> "BaseManager":
        queryset = BaseManager(cls)

        return queryset.order_by(*args)

    @classmethod
    def join_load(cls, *args) -> "BaseManager":
        queryset = BaseManager(cls)

        return queryset.join_load(*args)

    @classmethod
    def select_load(cls, *args) -> "BaseManager":
        queryset = BaseManager(cls)

        return queryset.select_load(*args)

    @classmethod
    async def get(cls) -> Table:
        queryset = BaseManager(cls)

        return await queryset.get()

    @classmethod
    async def first(cls) -> Table | None:
        queryset = BaseManager(cls)

        return await queryset.first()

    @classmethod
    async def all(cls) -> list[Table | None]:
        queryset = BaseManager(cls)

        return await queryset.all()

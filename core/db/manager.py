from typing import Type, TypeVar, Generic

from sqlalchemy import select, asc, desc, or_
from sqlalchemy.orm import DeclarativeBase, joinedload, selectinload

from core.db.engine import database


Table = TypeVar(
    "Table",
    bound='BaseModel',
)


class BaseManager(Generic[Table]):
    def __init__(
            self,
            model: Type[Table],
    ):
        self.model = model
        self.query = select(self.model)

    async def create(self, **kwargs) -> Table:
        async with database.async_session() as session:
            obj = self.model(**kwargs)
            session.add(obj)

            await session.commit()
            await session.refresh(obj)

        return obj

    async def update(self, **kwargs) -> list[Table] | Table:
        async with database.async_session() as session:
            stmt = await session.execute(self.query)

            all_objects = stmt.scalars().all()
            new_objects = list()

            for obj in all_objects:
                for key, value in kwargs.items():
                    setattr(obj, key, value)

                session.add(obj)
                new_objects.append(obj)

            await session.commit()

        return new_objects[0] if len(new_objects) == 1 else new_objects

    async def delete(self) -> None:
        async with database.async_session() as session:
            stmt = await session.execute(self.query)
            objects = stmt.scalars().all()

            for obj in objects:
                await session.delete(obj)

            await session.commit()

    def filter(self, **kwargs) -> "BaseManager":
        filters = []

        for key, value in kwargs.items():
            column = getattr(self.model, key.split("__")[0])

            if key.endswith("__or"):
                filters.append(or_(*[column == v for v in value]))
            elif key.endswith("__is"):
                filters.append(column.is_(value))
            elif key.endswith("__not"):
                filters.append(column != value)
            elif key.endswith("__null"):
                filters.append(column.is_(None) if value else column.isnot(None))
            elif key.endswith("__contains"):
                filters.append(column.like(f"%{value}%"))
            elif key.endswith("__icontains"):
                filters.append(column.ilike(f"%{value}%"))
            elif key.endswith("__in"):
                filters.append(column.in_(value))
            elif key.endswith("__not_in"):
                filters.append(~column.in_(value))
            elif key.endswith("__gt"):
                filters.append(column > value)
            elif key.endswith("__lt"):
                filters.append(column < value)
            elif key.endswith("__gte"):
                filters.append(column >= value)
            elif key.endswith("__lte"):
                filters.append(column <= value)
            else:
                filters.append(column == value)

        self.query = self.query.filter(*filters)

        return self

    def order_by(self, *args) -> "BaseManager":
        order_by_conditions = []

        for field_name in args:
            sort_order = asc if not field_name.startswith("-") else desc
            field_name = field_name.lstrip("-")
            field = getattr(self.model, field_name)
            order_by_conditions.append(sort_order(field))

        self.query = self.query.order_by(*order_by_conditions)

        return self

    def join_load(self, *args) -> "BaseManager":
        self.query = self.query.options(*(joinedload(getattr(self.model, model)) for model in args))

        return self

    def select_load(self, *args) -> "BaseManager":
        self.query = self.query.options(*(selectinload(getattr(self.model, model)) for model in args))

        return self

    async def get(self) -> Table:
        async with database.async_session() as session:
            result = await session.execute(self.query)

        return result.scalars().one()

    async def first(self) -> Table | None:
        async with database.async_session() as session:
            result = await session.execute(self.query)

        return result.scalars().first()

    async def all(self) -> list[Table | None]:
        async with database.async_session() as session:
            result = await session.execute(self.query)

        return result.scalars().all()

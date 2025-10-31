from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from core.db.model import BaseModel


class ConditionModel(BaseModel):
    __tablename__ = "condition"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f"<Condition(id={self.id} name={self.name})>"


class DistrictModel(BaseModel):
    __tablename__ = "district"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f"<District(id={self.id} name={self.name})>"


class MicroareaModel(BaseModel):
    __tablename__ = "microarea"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f"<Microarea(id={self.id} name={self.name})>"


class StreetModel(BaseModel):
    __tablename__ = "street"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f"<Street(id={self.id} name={self.name})>"

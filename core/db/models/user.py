import pytz

from datetime import datetime

from sqlalchemy import BigInteger, String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from core.db.model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    telegram_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_messages: Mapped[str] = mapped_column(String, nullable=False)
    agent_messages: Mapped[str] = mapped_column(String, nullable=False)
    filters: Mapped[JSON] = mapped_column(JSON, nullable=False)
    telegram_phone_number: Mapped[str] = mapped_column(String, nullable=False)
    data_created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.timezone("Europe/Kyiv")),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id})>"

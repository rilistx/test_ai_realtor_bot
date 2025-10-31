from aiogram.types import Message
from aiogram.filters import BaseFilter


class ContactFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.contact is not None:
            return True

        return False

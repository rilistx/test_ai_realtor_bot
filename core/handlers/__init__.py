from aiogram import Dispatcher

from .realtor import realtor_router


async def handlers(
        dispatcher: Dispatcher,
) -> None:
    dispatcher.include_router(
        router=realtor_router,
    )

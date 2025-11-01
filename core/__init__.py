__all__ = ["unpacker"]


from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeDefault

from core.db.initialization import init_db

from core.handlers import handlers
from core.commands.menu import commands
from core.config.loader import envs
from core.config.logger import logger


async def unpacker() -> None:
    logger()

    await init_db()

    bot = Bot(
        token=envs.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    storage = MemoryStorage()

    dispatcher = Dispatcher(
        bot=bot,
        storage=storage,
    )

    await handlers(
        dispatcher=dispatcher,
    )

    try:
        await bot.delete_webhook(
            drop_pending_updates=True,
        )
        await bot.delete_my_commands(
            scope=BotCommandScopeDefault(),
        )
        await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeDefault(),
        )
        await dispatcher.start_polling(
            bot,
            allowed_updates=dispatcher.resolve_used_update_types(),
        )
    finally:
        await bot.session.close()

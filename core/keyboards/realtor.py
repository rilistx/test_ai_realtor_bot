from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def realtor_button() -> ReplyKeyboardMarkup:
    button = KeyboardButton(
        text="☎️ Поділитися номером",
        request_contact=True,
    )

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard

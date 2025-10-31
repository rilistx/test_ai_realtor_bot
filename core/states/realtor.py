from aiogram.fsm.state import StatesGroup, State


class RealtorState(StatesGroup):
    START = State()
    QUESTION = State()
    PHONE = State()
    COMPLETED = State()

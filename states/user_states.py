from aiogram.dispatcher.filters.state import State, StatesGroup


class UserCreateStates(StatesGroup):
    telegram_id = State()
    first_name = State()
    last_name = State()
    phone_number = State()

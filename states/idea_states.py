from aiogram.dispatcher.filters.state import StatesGroup, State


class IdeaStates(StatesGroup):
    profile_id = State()
    text = State()


class Incentive(StatesGroup):
    profile_id = State()
    text = State()


class Objection(StatesGroup):
    profile_id = State()
    text = State()

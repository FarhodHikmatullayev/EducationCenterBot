from aiogram.dispatcher.filters.state import StatesGroup, State


class IdeaStates(StatesGroup):
    text = State()


class Incentive(StatesGroup):
    text = State()


class Objection(StatesGroup):
    text = State()

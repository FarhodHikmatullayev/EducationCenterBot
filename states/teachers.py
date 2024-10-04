from aiogram.dispatcher.filters.state import State, StatesGroup


class DeleteTeacherState(StatesGroup):
    teacher_id = State()


class CreateTeacherState(StatesGroup):
    user_id = State()
    first_name = State()
    last_name = State()
    experience = State()
    birth_year = State()

class UpdateTeacherState(StatesGroup):
    user_id = State()
    teacher_id = State()
    first_name = State()
    last_name = State()
    experience = State()
    birth_year = State()

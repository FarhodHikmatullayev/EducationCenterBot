from aiogram.dispatcher.filters.state import State, StatesGroup


class DeleteGroupState(StatesGroup):
    group_id = State()
    name = State()


class CreateGroupState(StatesGroup):
    name = State()
    teacher_id = State()


class UpdateGroupState(StatesGroup):
    group_id = State()
    name = State()
    teacher_id = State()


class RemoveStudentFromGroupState(StatesGroup):
    group_id = State()
    student_id = State()

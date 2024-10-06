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


class AddStudentToGroupState(StatesGroup):
    group_id = State()
    user_id = State()
    child_first_name = State()
    child_last_name = State()


class GetGroupState(StatesGroup):
    group_id = State()


class AddStudentToGroupStateForTeacher(StatesGroup):
    group_id = State()
    user_id = State()
    parent_id = State()
    child_first_name = State()
    child_last_name = State()


class DeleteStudentFromGroupStateForTeacher(StatesGroup):
    group_id = State()
    parent_id = State()
    user_id = State()


class GetGroupStateForAdmin(StatesGroup):
    group_id = State()
    teacher_id = State()

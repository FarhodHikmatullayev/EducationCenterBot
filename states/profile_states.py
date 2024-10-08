from aiogram.dispatcher.filters.state import State, StatesGroup


class UpdateAdminProfileState(StatesGroup):
    admin_id = State()
    first_name = State()
    last_name = State()
    phone_number = State()


class UpdateTeacherProfileState(StatesGroup):
    user_id = State()
    teacher_profile_id = State()
    first_name = State()
    last_name = State()
    phone_number = State()
    experience = State()
    birth_year = State()


class UpdateParentProfileState(StatesGroup):
    user_id = State()
    parent_profile_id = State()
    child_first_name = State()
    child_last_name = State()
    phone_number = State()


class GetProfileState(StatesGroup):
    profile_id = State()


class GetProfileStateForRating(StatesGroup):
    profile_id = State()

class GetProfileStateForProfile(StatesGroup):
    profile_id = State()

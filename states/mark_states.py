from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateMarkState(StatesGroup):
    student_id = State()
    kayfiyat = State()
    tartib = State()
    faollik = State()
    vaqtida_kelish = State()
    dars_qoldirmaslik = State()
    vazifa_bajarilganligi = State()
    darsni_ozlashtirish = State()
    description = State()

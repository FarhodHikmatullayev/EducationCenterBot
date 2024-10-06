from idlelib.window import add_windows_to_menu

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.all_students import all_students_in_group
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.group_actions import group_actions_for_teachers
from keyboards.default.menu_keyboards import back_to_menu, go_back_default_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from keyboards.inline.mark_keyboards import marks_keyboard
from loader import dp, db, bot
from states.groups import GetGroupState
from states.mark_states import CreateMarkState


@dp.message_handler(text="✨ Guruhdagi o'quvchilarni baholash", state=GetGroupState.group_id)
async def mark_function(message: types.Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.answer(text="🚫 Sizda botdan foydalanish uchun ruxsat mavjud emas,\n"
                                  "📝 Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak 👇",
                             reply_markup=go_registration_default_keyboard)
    else:
        user = users[0]
        user_role = user['role']
        if user_role != 'teacher':
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            data = await state.get_data()
            group_id = data.get('group_id')
            markup = await all_students_in_group(group_id=group_id)
            await message.answer(text="Baholash uchun o'quvchilardan birini tanlang 👇", reply_markup=markup)
            await CreateMarkState.student_id.set()


@dp.message_handler(state=[CreateMarkState.student_id], text="🔙 Orqaga")
async def get_group_id(message: types.Message, state: FSMContext):
    await GetGroupState.group_id.set()
    await message.answer(text="Amallardan birini tanlang 👇", reply_markup=group_actions_for_teachers)


@dp.message_handler(state=CreateMarkState.student_id)
async def get_student_id(message: types.Message, state: FSMContext):
    student_full_name = message.text
    student_first_name = student_full_name.split()[0]
    student_last_name = student_full_name.split()[1]
    parent_profiles = await db.select_parent_profiles(child_first_name=student_first_name,
                                                      child_last_name=student_last_name)
    if not parent_profiles:
        await message.answer(text="⚠️ Bu o'quvchi allaqachon guruhda chiqarib tashlangan",
                             reply_markup=go_back_default_keyboard)
        return
    parent_profile = parent_profiles[0]
    student_id = parent_profile['id']
    student_marks = await db.select_today_marks(student_id=student_id)
    if student_marks:
        await message.answer(
            text="⚠️ Bu o'quvchiga allaqachon baho qo'ydingiz, bir dars uchun bir marta baho qo'yish mumkin",
            reply_markup=go_back_default_keyboard)
        return
    await state.update_data(student_id=student_id)
    await message.answer(text="Bosh menyuga qaytish uchun 'Bosh Menyu' tugmasini bosing 👇", reply_markup=back_to_menu)
    await message.answer(text="O'quvchining darsdagi kayfiyatiga baho bering:", reply_markup=marks_keyboard)
    await CreateMarkState.kayfiyat.set()


@dp.callback_query_handler(state=CreateMarkState.kayfiyat)
async def get_kayfiyat_mark(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(kayfiyat=mark)
    await call.message.edit_text(text="O'quvchining tartibiga baho bering:", reply_markup=marks_keyboard)
    await CreateMarkState.tartib.set()


@dp.callback_query_handler(state=CreateMarkState.tartib)
async def get_tartib_mark(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(tartib=mark)
    await call.message.edit_text(text="O'quvchining darsdagi faolligiga baho bering:", reply_markup=marks_keyboard)
    await CreateMarkState.faollik.set()


@dp.callback_query_handler(state=CreateMarkState.faollik)
async def get_faollik_mark(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(faollik=mark)
    await call.message.edit_text(text="O'quvchining darsga vaqtida kelishiga baho bering:", reply_markup=marks_keyboard)
    await CreateMarkState.vaqtida_kelish.set()


@dp.callback_query_handler(state=CreateMarkState.vaqtida_kelish)
async def get_vaqtida_kelish_mark(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(vaqtida_kelish=mark)
    await call.message.edit_text(text="O'quvchining dars qoldirmasligiga baho bering:", reply_markup=marks_keyboard)
    await CreateMarkState.dars_qoldirmaslik.set()


@dp.callback_query_handler(state=CreateMarkState.dars_qoldirmaslik)
async def get_dars_qoldirmaslik_mark(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(dars_qoldirmaslik=mark)
    await call.message.edit_text(text="O'quvchining vazifalarni bajarishiga baho bering:", reply_markup=marks_keyboard)
    await CreateMarkState.vazifa_bajarilganligi.set()


@dp.callback_query_handler(state=CreateMarkState.vazifa_bajarilganligi)
async def get_vazifa_bajarganlik_mark(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(vazifa_bajarilganligi=mark)
    await call.message.edit_text(text="O'quvchining darsni o'zlashtirishiga baho bering:", reply_markup=marks_keyboard)
    await CreateMarkState.darsni_ozlashtirish.set()


@dp.callback_query_handler(state=CreateMarkState.darsni_ozlashtirish, text="yes")
async def confirm_getting_description(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="✍️ Izoh yozing", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await CreateMarkState.description.set()


@dp.callback_query_handler(state=CreateMarkState.darsni_ozlashtirish, text='no')
async def cancel_getting_description(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    student_id = data.get("student_id")
    kayfiyat = data.get("kayfiyat")
    tartib = data.get("tartib")
    faollik = data.get("faollik")
    vaqtida_kelish = data.get("vaqtida_kelish")
    dars_qoldirmaslik = data.get("dars_qoldirmaslik")
    vazifa_bajarilganligi = data.get("vazifa_bajarilganligi")
    darsni_ozlashtirish = data.get("darsni_ozlashtirish")

    parent_profile = await db.select_parent_profile(profile_id=student_id)
    first_name = parent_profile['child_first_name']
    last_name = parent_profile['child_last_name']

    text = (f"Siz quyidagicha baholadingiz: ⭐\n"
            f"👤 O'quvchi: {first_name} {last_name}\n"
            f"😊 Kayfiyati: {kayfiyat}\n"
            f"📚 Tartibi: {tartib}\n"
            f"💪 Darsdagi faolligi: {faollik}\n"
            f"⏰ Darsga vaqtida kelishi: {vaqtida_kelish}\n"
            f"🚫 Dars qoldirmasligi: {dars_qoldirmaslik}\n"
            f"✅ Vazifalarni bajarganligi: {vazifa_bajarilganligi}\n"
            f"📖 Darsni o'zlashtirishi: {darsni_ozlashtirish}\n")
    await call.message.edit_text(text=text)
    await call.message.answer(text="Bu bahoni saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)
    await CreateMarkState.description.set()


@dp.callback_query_handler(state=CreateMarkState.darsni_ozlashtirish)
async def get_darsni_ozlashtirishi_mark(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(darsni_ozlashtirish=mark)
    await call.message.edit_text(text="Nega bunday baholaganingizga izoh yozasizmi?", reply_markup=confirm_keyboard)


@dp.callback_query_handler(state=CreateMarkState.description, text="yes")
async def save_mark_function(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    student_id = data.get("student_id")
    kayfiyat = data.get("kayfiyat")
    tartib = data.get("tartib")
    faollik = data.get("faollik")
    vaqtida_kelish = data.get("vaqtida_kelish")
    dars_qoldirmaslik = data.get("dars_qoldirmaslik")
    vazifa_bajarilganligi = data.get("vazifa_bajarilganligi")
    darsni_ozlashtirish = data.get("darsni_ozlashtirish")
    description = data.get('description')

    mark = await db.create_daily_mark(
        student_id=student_id,
        kayfiyat=kayfiyat,
        tartib=tartib,
        faollik=faollik,
        vaqtida_kelish=vaqtida_kelish,
        dars_qoldirmaslik=dars_qoldirmaslik,
        vazifa_bajarilganligi=vazifa_bajarilganligi,
        darsni_ozlashtirish=darsni_ozlashtirish,
        description=description
    )

    text = (f"Farzandingizning bugungi baholari: 🌟\n"
            f"😊 Darsda kayfiyati: {kayfiyat}\n"
            f"📚 Tartibi: {tartib}\n"
            f"💪 Darsdagi faolligi: {faollik}\n"
            f"⏰ Darsga vaqtida kelishi: {vaqtida_kelish}\n"
            f"🚫 Dars qoldirmasligi: {dars_qoldirmaslik}\n"
            f"✅ Vazifalarning bajarilganligi: {vazifa_bajarilganligi}\n"
            f"📖 Darsni o'zlashtirishi: {darsni_ozlashtirish}")

    if description:
        text += f"\n💬 Izoh: {description}"

    parent_profile = await db.select_parent_profile(profile_id=student_id)
    user_id = parent_profile['user_id']
    user = await db.select_user(user_id=user_id)
    user_telegram_id = user['telegram_id']
    await bot.send_message(chat_id=user_telegram_id, text=text)

    await call.message.answer(text="✅ Baho saqlandi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=CreateMarkState.description, text="no")
async def cancel_saving_mark(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Bahoni saqlash bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=CreateMarkState.description)
async def get_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    data = await state.get_data()
    student_id = data.get("student_id")
    kayfiyat = data.get("kayfiyat")
    tartib = data.get("tartib")
    faollik = data.get("faollik")
    vaqtida_kelish = data.get("vaqtida_kelish")
    dars_qoldirmaslik = data.get("dars_qoldirmaslik")
    vazifa_bajarilganligi = data.get("vazifa_bajarilganligi")
    darsni_ozlashtirish = data.get("darsni_ozlashtirish")
    description = data.get('description')

    parent_profile = await db.select_parent_profile(profile_id=student_id)
    first_name = parent_profile['child_first_name']
    last_name = parent_profile['child_last_name']

    text = (f"Siz quyidagicha baholadingiz: ⭐\n"
            f"👤 O'quvchi: {first_name} {last_name}\n"
            f"😊 Kayfiyati: {kayfiyat}\n"
            f"📚 Tartibi: {tartib}\n"
            f"💪 Darsdagi faolligi: {faollik}\n"
            f"⏰ Darsga vaqtida kelishi: {vaqtida_kelish}\n"
            f"🚫 Dars qoldirmasligi: {dars_qoldirmaslik}\n"
            f"✅ Vazifalarni bajarganligi: {vazifa_bajarilganligi}\n"
            f"📖 Darsni o'zlashtirishi: {darsni_ozlashtirish}\n"
            f"💬 Izohingiz: {description}")
    await message.answer(text=text)
    await message.answer(text="Bu bahoni saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)

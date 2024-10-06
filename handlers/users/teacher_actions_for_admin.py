from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.all_teachers import all_teachers_default_keyboard
from keyboards.default.all_users import all_users_default_keyboard
from keyboards.default.change_profile_keyboards import next_change_default_keyboard
from keyboards.default.confirm_action_for_teacher import delete_teacher_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu, go_back_default_keyboard
from keyboards.default.teacher_actions import teacher_actions_default_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from loader import dp, db, bot
from states.teachers import DeleteTeacherState, CreateTeacherState, UpdateTeacherState


# for delete
@dp.message_handler(text="🗑️ O'chirish", state=DeleteTeacherState.teacher_id)
async def delete_teacher_final_function(message: types.Message, state: FSMContext):
    data = await state.get_data()
    teacher_id = data.get("teacher_id")
    teacher = await db.select_teacher_profile(profile_id=teacher_id)
    if teacher:
        groups = await db.select_groups(teacher_id=teacher_id)
        for group in groups:
            await db.update_group(
                group_id=group["id"],
                teacher_id=None,
            )
        user_id = teacher['user_id']
        await db.update_user(user_id=user_id, role='user')
        await db.delete_teacher_profile(profile_id=teacher_id)
        await message.answer(text="📣 O'qituvchi muvaffaqiyatli o'chirildi ✅", reply_markup=back_to_menu)
    else:
        await message.answer(text="📢 Bu O'qituvchi allaqachon o'chirilgan", reply_markup=back_to_menu)
    await state.finish()


@dp.message_handler(text="🗑️ O'qituvchini o'chirish", state="*")
async def delete_teacher(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.answer(text="🚫 Sizda botdan foydalanish uchun ruxsat mavjud emas,\n"
                                  "📝 Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak 👇",
                             reply_markup=go_registration_default_keyboard)
    else:
        user = users[0]
        user_role = user['role']
        if user_role != 'admin':
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            markup = await all_teachers_default_keyboard()
            await message.answer(text="O'chirmoqchi bo'lgan o'qituvchini tanlang 👇", reply_markup=markup)
            await DeleteTeacherState.teacher_id.set()


@dp.message_handler(text="🔙 Orqaga", state=DeleteTeacherState.teacher_id)
async def back_to_actions(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Kerakli amalni tanlang 👇", reply_markup=teacher_actions_default_keyboard)


@dp.message_handler(text="🔙 O'qituvchilarga qaytish", state=DeleteTeacherState.teacher_id, user_id=ADMINS)
async def back_to_groups_list(message: types.Message, state: FSMContext):
    markup = await all_teachers_default_keyboard()
    await message.answer(text="O'chirmoqchi bo'lgan o'qituvchini tanlang 👇", reply_markup=markup)
    await DeleteTeacherState.teacher_id.set()


@dp.message_handler(state=DeleteTeacherState.teacher_id)
async def delete_teacher(message: types.Message, state: FSMContext):
    teacher_full_name = message.text

    teacher_first_name = teacher_full_name.split()[0]
    teacher_last_name = teacher_full_name.split()[1]

    teacher_profiles = await db.select_teacher_profiles(first_name=teacher_first_name, last_name=teacher_last_name)
    teacher = teacher_profiles[0]
    await state.update_data(teacher_id=teacher['id'])

    teacher_birth_year = teacher['birth_year']
    if not teacher_birth_year:
        teacher_age = "Hali kiritilmagan"
    else:
        teacher_age = datetime.now().year - teacher_birth_year
    teacher_experience = teacher['experience']
    if not teacher_experience:
        teacher_experience = "Hali kiritilmagan"

    teacher_groups = await db.select_groups(teacher_id=teacher['id'])
    if teacher_groups:
        all_groups = ""
        tr = 0
        for group in teacher_groups:
            tr += 1
            all_groups += f"\n  {tr}.{group['name']}"
    else:
        all_groups = "Hali guruh belgilanmagan"

    text = (f"📚 O'qituvchi ma'lumotlari 👇\n"
            f"👨‍🏫 Ismi: {teacher_first_name}\n"
            f"📜 Familiyasi: {teacher_last_name}\n"
            f"🕒 Yoshi: {teacher_age}\n"
            f"🧑‍💼 Ish staji: {teacher_experience} yil\n"
            f"📖 Guruhlari: {all_groups}\n")
    await message.answer(text=text)
    await message.answer(text="💬 O'qituvchini o'chirasizmi?\n"
                              "O'chirish tumasini bosing 👇", reply_markup=delete_teacher_default_keyboard)


# for create
@dp.message_handler(text="➕ O'qituvchi qo'shish", state="*")
async def start_adding_teacher(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.answer(text="🚫 Sizda botdan foydalanish uchun ruxsat mavjud emas,\n"
                                  "📝 Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak 👇",
                             reply_markup=go_registration_default_keyboard)
    else:
        user = users[0]
        user_role = user['role']
        if user_role != 'admin':
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
            return
        else:
            markup = await all_users_default_keyboard()
            await message.answer(
                text="🆕 Yangi o'qituvchi qo'shish uchun foydalanuvchilardan birini tanlang: 👇",
                reply_markup=markup
            )
            await CreateTeacherState.first_name.set()


@dp.message_handler(state=CreateTeacherState.first_name)
async def get_teacher_full_name(message: types.Message, state: FSMContext):
    teacher_full_name = message.text
    first_name = teacher_full_name.split()[0]
    last_name = teacher_full_name.split()[1]
    users = await db.select_users(full_name=teacher_full_name)
    if not users:
        await message.answer(text="⚠️ Bu foydalanuvchi allaqachon o'chirib yuborilgan",
                             reply_markup=go_back_default_keyboard)
        return

    await state.update_data(first_name=first_name, last_name=last_name, user_id=users[0]['id'])
    await message.answer(text="🕒 O'qituchi uchun ish staji kiriting (yil hisoboda: misol-3):\n"
                              "👉 Agar ish stajini kiritmoqchi bo'lmasangiz, 'keyingi' tugmasini bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await CreateTeacherState.experience.set()


@dp.message_handler(state=CreateTeacherState.experience, text="Keyingi 🔜")
@dp.message_handler(state=CreateTeacherState.experience)
async def get_teacher_experience(message: types.Message, state: FSMContext):
    teacher_experience = message.text
    if teacher_experience != "Keyingi 🔜":
        try:
            teacher_experience = int(teacher_experience)
            if teacher_experience < 1 or teacher_experience > 30:
                await message.answer(text="⚠️ Iltimos, staj uchun 1 dan 30 gacha son kiritishingiz kerak:",
                                     reply_markup=back_to_menu)
                return
        except:
            await message.answer(text="⚠️ Siz staj uchun son kiritishingiz kerak:", reply_markup=back_to_menu)
            return
        await state.update_data(experience=teacher_experience)
    await message.answer(text="📅 O'qituvchi tug'ilgan yili kiriting:\n"
                              "👉 Agar tug'ilgan yilni kiritishni istamasangiz, 'Keyingi' tugmasini bosing 👇",
                         reply_markup=next_change_default_keyboard
                         )
    await CreateTeacherState.birth_year.set()


@dp.callback_query_handler(text='yes', state=CreateTeacherState.birth_year)
async def save_teacher(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    experience = data.get("experience")
    birth_year = data.get("birth_year")

    teacher_profile = await db.create_teacher_profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        experience=experience,
        birth_year=birth_year
    )

    user = await db.update_user(
        user_id=user_id,
        role='teacher'
    )

    await call.message.answer(text="✅ O'qituvchi qo'shildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=CreateTeacherState.birth_year, text="no")
async def cancel_saving_teacher(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="Saqlash rad etildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=CreateTeacherState.birth_year, text="Keyingi 🔜")
@dp.message_handler(state=CreateTeacherState.birth_year)
async def get_teacher_birth_year(message: types.Message, state: FSMContext):
    birth_year = message.text

    if birth_year != "Keyingi 🔜":
        try:
            birth_year = int(birth_year)
            if birth_year > 2010 or birth_year < 1970:
                await message.answer(
                    text="Iltimos, tug'ilgan yil uchun 1970 dan katta 2010 dan kichik son kiritishingiz kerak:",
                    reply_markup=back_to_menu)
                return
        except:
            await message.answer(text="Iltimos, tug'ilgan yil uchun son kiritishingiz kerak:",
                                 reply_markup=back_to_menu)
            return
        await state.update_data(birth_year=birth_year)
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    experience = data.get("experience")
    birth_year = data.get("birth_year")
    if not experience:
        experience = "Hali kiritilmagan"
    if not birth_year:
        birth_year = "Hali kiritilmagan"
    text = (f"📚 O'qituvchi ma'lumotlari quyidagicha bo'ladi 👇\n"
            f"🧑‍💼 Ism: {first_name}\n"
            f"👤 Familiya: {last_name}\n"
            f"💼 Ish staji(yil): {experience}\n"
            f"📅 Tug'ilgan yili: {birth_year}")
    await message.answer(text=text)
    await message.answer(text="Saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)


# for update
@dp.message_handler(text="✏️ O'qituvchini o'zgartirish", state="*")
async def start_adding_teacher(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.answer(text="🚫 Sizda botdan foydalanish uchun ruxsat mavjud emas,\n"
                                  "📝 Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak 👇",
                             reply_markup=go_registration_default_keyboard)
    else:
        user = users[0]
        user_role = user['role']
        if user_role != 'admin':
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
            return
        else:
            markup = await all_teachers_default_keyboard()
            await message.answer(
                text="🆕 O'qituvchini o'zgartirish uchun ulardan birin tanlang: 👇",
                reply_markup=markup
            )
            await UpdateTeacherState.teacher_id.set()


@dp.message_handler(state=UpdateTeacherState.teacher_id)
async def get_teacher_id(message: types.Message, state: FSMContext):
    teacher_full_name = message.text
    first_name = teacher_full_name.split()[0]
    last_name = teacher_full_name.split()[1]
    teacher_profiles = await db.select_teacher_profiles(first_name=first_name, last_name=last_name)
    if not teacher_profiles:
        await message.answer(text="⚠️ Bu O'qituvchi allaqachon o'chirib yuborilgan",
                             reply_markup=go_back_default_keyboard)
        return

    await state.update_data(
        first_name=first_name,
        last_name=last_name,
        teacher_id=teacher_profiles[0]['id'],
        experience=teacher_profiles[0]['experience'],
        birth_year=teacher_profiles[0]['birth_year']
    )
    await message.answer(text="🔤 O'qituvchi uchun yangi ism kiriting:\n"
                              "❌ Agar ismni o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmasini bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await UpdateTeacherState.first_name.set()


@dp.message_handler(state=UpdateTeacherState.first_name, text="Keyingi 🔜")
@dp.message_handler(state=UpdateTeacherState.first_name)
async def get_teacher_first_name(message: types.Message, state: FSMContext):
    first_name = message.text
    if first_name != "Keyingi 🔜":
        await state.update_data(first_name=first_name)
    await message.answer(text="🔤 O'qituvchi uchun yangi familiya kiriting:\n"
                              "❌ Agar familiyani o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmasini bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await UpdateTeacherState.last_name.set()


@dp.message_handler(state=UpdateTeacherState.last_name, text="Keyingi 🔜")
@dp.message_handler(state=UpdateTeacherState.last_name)
async def get_teacher_last_name(message: types.Message, state: FSMContext):
    last_name = message.text
    if last_name != "Keyingi 🔜":
        await state.update_data(last_name=last_name)

    await message.answer(text="🕒 O'qituchi uchun yangi ish staji kiriting (yil hisoboda: misol-3):\n"
                              "👉 Agar yangi ish staji kiritmoqchi bo'lmasangiz, 'keyingi' tugmasini bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await UpdateTeacherState.experience.set()


@dp.message_handler(state=UpdateTeacherState.experience, text="Keyingi 🔜")
@dp.message_handler(state=UpdateTeacherState.experience)
async def get_teacher_experience(message: types.Message, state: FSMContext):
    teacher_experience = message.text
    if teacher_experience != "Keyingi 🔜":
        try:
            teacher_experience = int(teacher_experience)
            if teacher_experience < 1 or teacher_experience > 30:
                await message.answer(text="⚠️ Iltimos, staj uchun 1 dan 30 gacha son kiritishingiz kerak:",
                                     reply_markup=back_to_menu)
                return
        except:
            await message.answer(text="⚠️ Siz staj uchun son kiritishingiz kerak:", reply_markup=back_to_menu)
            return
        await state.update_data(experience=teacher_experience)
    await message.answer(text="📅 O'qituvchi uchun yangi tug'ilgan yil kiriting:\n"
                              "👉 Agar tug'ilgan yilni o'zgartirishni istamasangiz, 'Keyingi' tugmasini bosing 👇",
                         reply_markup=next_change_default_keyboard
                         )
    await UpdateTeacherState.birth_year.set()


@dp.callback_query_handler(text='yes', state=UpdateTeacherState.birth_year)
async def update_teacher(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    teacher_id = data.get('teacher_id')
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    experience = data.get("experience")
    birth_year = data.get("birth_year")

    teacher_profile = await db.update_teacher_profile(
        profile_id=teacher_id,
        first_name=first_name,
        last_name=last_name,
        experience=experience,
        birth_year=birth_year
    )
    teacher_profile = await db.select_teacher_profile(profile_id=teacher_id)
    user = await db.update_user(
        user_id=teacher_profile['user_id'],
        full_name=f"{first_name} {last_name}",
    )

    await call.message.answer(text="✅ O'qituvchi o'zgartirildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=UpdateTeacherState.birth_year, text="no")
async def cancel_updating_teacher(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ O'zgartirish rad etildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=UpdateTeacherState.birth_year, text="Keyingi 🔜")
@dp.message_handler(state=UpdateTeacherState.birth_year)
async def get_teacher_birth_year(message: types.Message, state: FSMContext):
    birth_year = message.text

    if birth_year != "Keyingi 🔜":
        try:
            birth_year = int(birth_year)
            if birth_year > 2010 or birth_year < 1970:
                await message.answer(
                    text="Iltimos, tug'ilgan yil uchun 1970 dan katta 2010 dan kichik son kiritishingiz kerak:",
                    reply_markup=back_to_menu)
                return
        except:
            await message.answer(text="Iltimos, tug'ilgan yil uchun son kiritishingiz kerak:",
                                 reply_markup=back_to_menu)
            return
        await state.update_data(birth_year=birth_year)
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    experience = data.get("experience")
    birth_year = data.get("birth_year")
    if not experience:
        experience = "Hali kiritilmagan"
    if not birth_year:
        birth_year = "Hali kiritilmagan"
    text = (f"📚 O'qituvchi ma'lumotlari quyidagicha bo'ladi 👇\n"
            f"🧑‍💼 Ism: {first_name}\n"
            f"👤 Familiya: {last_name}\n"
            f"💼 Ish staji(yil): {experience}\n"
            f"📅 Tug'ilgan yili: {birth_year}")
    await message.answer(text=text)
    await message.answer(text="Saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)

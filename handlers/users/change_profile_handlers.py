from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.change_profile_keyboards import next_change_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu
from keyboards.inline.confirmation import confirm_keyboard
from loader import dp, db, bot
from states.profile_states import UpdateAdminProfileState, UpdateTeacherProfileState, UpdateParentProfileState


@dp.message_handler(text="✏️ Profilni o'zgartirish", state="*")
async def change_profile_function(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.reply(text="🚫 Sizda botdan foydalanish uchun ruxsat mavjud emas,\n"
                                 "📝 Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak 👇",
                            reply_markup=go_registration_default_keyboard)
    else:
        user = users[0]
        user_role = user['role']
        if user_role == 'admin':
            full_name = user['full_name']
            admin_id = user['id']
            first_name = full_name.split()[0]
            last_name = full_name.split()[1]
            phone = user['phone']
            await state.update_data(
                admin_id=admin_id,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone,
            )

            await message.answer(text="🆕 Yangi ism kiriting:\n"
                                      "Agar ismni o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmani bosing 👇",
                                 reply_markup=next_change_default_keyboard)
            await UpdateAdminProfileState.first_name.set()
        elif user_role == 'teacher':
            full_name = user['full_name']
            teacher_id = user['id']
            first_name = full_name.split()[0]
            last_name = full_name.split()[1]
            phone = user['phone']
            teacher_profiles = await db.select_teacher_profiles(user_id=teacher_id)
            teacher_profile = teacher_profiles[0]
            teacher_profile_id = teacher_profile['id']
            birth_year = teacher_profile['birth_year']
            experience = teacher_profile['experience']
            await state.update_data(
                user_id=teacher_id,
                teacher_profile_id=teacher_profile_id,
                first_name=first_name,
                last_name=last_name,
                birth_year=birth_year,
                phone_number=phone,
                experience=experience,
            )
            await message.answer(text="🆕 Yangi ism kiriting:\n"
                                      "Agar ismni o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmani bosing 👇",
                                 reply_markup=next_change_default_keyboard)
            await UpdateTeacherProfileState.first_name.set()

        elif user_role == 'parent':
            user_id = user['id']
            phone_number = user['phone']
            parent_profiles = await db.select_parent_profiles(user_id=user_id)
            parent_profile = parent_profiles[0]
            child_first_name = parent_profile['child_first_name']
            child_last_name = parent_profile['child_last_name']
            parent_profile_id = parent_profile['id']
            await state.update_data(
                user_id=user_id,
                parent_profile_id=parent_profile_id,
                child_first_name=child_first_name,
                child_last_name=child_last_name,
                phone_number=phone_number,
            )
            await message.answer(text="🆕 Farzandingiz uchun yangi ism kiriting:\n"
                                      "Agar ismni o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmani bosing 👇",
                                 reply_markup=next_change_default_keyboard)
            await UpdateParentProfileState.child_first_name.set()

        else:
            text = "❌ Sizda hali profil mavjud emas"
            await message.reply(text=text)
            return


# for admins
@dp.message_handler(state=UpdateAdminProfileState.first_name, text="Keyingi 🔜")
@dp.message_handler(state=UpdateAdminProfileState.first_name)
async def get_admin_first_name_function(message: types.Message, state: FSMContext):
    first_name = message.text
    if first_name != "Keyingi 🔜":
        await state.update_data(first_name=first_name)
    await message.answer(text="🆕 Yangi familiya kiriting:\n"
                              "Agar familiyani o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmani bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await UpdateAdminProfileState.last_name.set()


@dp.message_handler(state=UpdateAdminProfileState.last_name, text="Keyingi 🔜")
@dp.message_handler(state=UpdateAdminProfileState.last_name)
async def get_admin_last_name_function(message: types.Message, state: FSMContext):
    last_name = message.text
    if last_name != "Keyingi 🔜":
        await state.update_data(last_name=last_name)
    await message.answer(text="🆕 Yangi telefon raqam kiriting:\n"
                              "Agar telefon raqamni o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmani bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await UpdateAdminProfileState.phone_number.set()


@dp.callback_query_handler(text='yes', state=UpdateAdminProfileState.phone_number)
async def save_changes_admin_profile_function(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone_number = data.get("phone_number")
    admin_id = data.get('admin_id')
    full_name = f"{first_name} {last_name}"
    admin_user = await db.update_user(
        user_id=admin_id,
        full_name=full_name,
        phone=phone_number,
    )
    await call.message.answer(text="✅ Profil muvaffaqiyatli o'zgartirildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text='no', state=UpdateAdminProfileState.phone_number)
async def cancel_changes_admin_profile_function(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Profil o'zgarishini rad etdingiz", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=UpdateAdminProfileState.phone_number, text="Keyingi 🔜")
@dp.message_handler(state=UpdateAdminProfileState.phone_number)
async def get_admin_phone_number_function(message: types.Message, state: FSMContext):
    phone_number = message.text
    if phone_number != "Keyingi 🔜":
        await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone_number = data.get("phone_number")

    text = (f"🔄 Profilingiz o'zgarishlardan so'ng quyidagicha bo'ladi 👇\n"
            f"🧑‍💼 Ismingiz: {first_name}\n"
            f"👤 Familiyangiz: {last_name}\n"
            f"📞 Telefon raqamingiz: {phone_number}\n")
    await message.answer(text=text)
    await message.answer(text="Saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)


# for teachers
@dp.message_handler(state=UpdateTeacherProfileState.first_name, text="Keyingi 🔜")
@dp.message_handler(state=UpdateTeacherProfileState.first_name)
async def get_teacher_first_name_function(message: types.Message, state: FSMContext):
    first_name = message.text
    if first_name != "Keyingi 🔜":
        await state.update_data(first_name=first_name)
    await message.answer(text="🆕 Yangi familiya kiriting:\n"
                              "Agar familiyani o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmani bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await UpdateTeacherProfileState.last_name.set()


@dp.message_handler(state=UpdateTeacherProfileState.last_name, text="Keyingi 🔜")
@dp.message_handler(state=UpdateTeacherProfileState.last_name)
async def get_teacher_last_name_function(message: types.Message, state: FSMContext):
    last_name = message.text
    if last_name != "Keyingi 🔜":
        await state.update_data(last_name=last_name)
    await message.answer(text="🆕 Yangi telefon raqam kiriting:\n"
                              "Agar telefon raqamni o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmani bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await UpdateTeacherProfileState.phone_number.set()


@dp.message_handler(state=UpdateTeacherProfileState.phone_number, text="Keyingi 🔜")
@dp.message_handler(state=UpdateTeacherProfileState.phone_number)
async def get_teacher_phone_number_function(message: types.Message, state: FSMContext):
    phone_number = message.text
    if phone_number != "Keyingi 🔜":
        await state.update_data(phone_number=phone_number)
    await message.answer(text="🆕 Yangi tug'ilgan yil kiriting (misol: 2000):\n"
                              "Agar tug'ilgan yilingizni o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmani bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await UpdateTeacherProfileState.birth_year.set()


@dp.message_handler(state=UpdateTeacherProfileState.birth_year, text="Keyingi 🔜")
@dp.message_handler(state=UpdateTeacherProfileState.birth_year)
async def get_teacher_birth_year_function(message: types.Message, state: FSMContext):
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
    await message.answer(text="🆕 Yangi staj kiriting (yilda kiriting, misol: 3):\n"
                              "Agar stajingizni o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmani bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await UpdateTeacherProfileState.experience.set()


@dp.callback_query_handler(text='yes', state=UpdateTeacherProfileState.experience)
async def save_changes_teacher_profile_function(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone_number = data.get("phone_number")
    user_id = data.get("user_id")
    teacher_profile_id = data.get("teacher_profile_id")
    experience = data.get("experience")
    birth_year = data.get("birth_year")

    full_name = f"{first_name} {last_name}"
    admin_user = await db.update_user(
        user_id=user_id,
        full_name=full_name,
        phone=phone_number,
    )

    teacher_profile = await db.update_teacher_profile(
        profile_id=teacher_profile_id,
        first_name=first_name,
        last_name=last_name,
        birth_year=birth_year,
        experience=experience,
    )

    await call.message.answer(text="✅ Profil muvaffaqiyatli o'zgartirildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text='no', state=UpdateTeacherProfileState.experience)
async def cancel_changes_teacher_profile_function(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Profil o'zgarishini rad etdingiz", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=UpdateTeacherProfileState.experience, text="Keyingi 🔜")
@dp.message_handler(state=UpdateTeacherProfileState.experience)
async def get_teacher_experience_function(message: types.Message, state: FSMContext):
    experience = message.text
    if experience != "Keyingi 🔜":
        try:
            experience = int(experience)
            if experience < 1 or experience > 30:
                await message.answer(text="⚠️ Iltimos, staj uchun 1 dan 30 gacha son kiritishingiz kerak:",
                                     reply_markup=back_to_menu)
                return
        except:
            await message.answer(text="⚠️ Siz staj uchun son kiritishingiz kerak:", reply_markup=back_to_menu)
            return
        await state.update_data(experience=experience)
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone_number = data.get("phone_number")
    experience = data.get("experience")
    birth_year = data.get("birth_year")

    text = (f"🔄 Profilingiz o'zgarishlardan so'ng quyidagicha bo'ladi 👇\n"
            f"🧑‍💼 Ismingiz: {first_name}\n"
            f"👤 Familiyangiz: {last_name}\n"
            f"📞 Telefon raqamingiz: {phone_number}\n"
            f"💼 Ish stajingiz: {experience} yil\n"
            f"📅 Tug'ilgan yilingiz: {birth_year}")
    await message.answer(text=text)
    await message.answer(text="Saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)


# for parents
@dp.message_handler(state=UpdateParentProfileState.child_first_name, text="Keyingi 🔜")
@dp.message_handler(state=UpdateParentProfileState.child_first_name)
async def get_parent_child_first_name_function(message: types.Message, state: FSMContext):
    child_first_name = message.text
    if child_first_name != "Keyingi 🔜":
        await state.update_data(child_first_name=child_first_name)
    await message.answer(text="🆕 Farzandingiz uchun yangi familiya kiriting:\n"
                              "Agar familiyani o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmani bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await UpdateParentProfileState.child_last_name.set()


@dp.message_handler(state=UpdateParentProfileState.child_last_name, text="Keyingi 🔜")
@dp.message_handler(state=UpdateParentProfileState.child_last_name)
async def get_parent_child_last_name_function(message: types.Message, state: FSMContext):
    child_last_name = message.text
    if child_last_name != "Keyingi 🔜":
        await state.update_data(child_last_name=child_last_name)
    await message.answer(text="🆕 Yangi telefon raqam kiriting:\n"
                              "Agar telefon raqamni o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmani bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await UpdateParentProfileState.phone_number.set()


@dp.callback_query_handler(text='yes', state=UpdateParentProfileState.phone_number)
async def save_changes_parent_profile_function(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    child_first_name = data.get("child_first_name")
    child_last_name = data.get("child_last_name")
    phone_number = data.get("phone_number")
    user_id = data.get("user_id")
    parent_profile_id = data.get("parent_profile_id")
    admin_user = await db.update_user(
        user_id=user_id,
        phone=phone_number,
    )
    parent_profile = await db.update_parent_profile(
        profile_id=parent_profile_id,
        child_first_name=child_first_name,
        child_last_name=child_last_name,
    )
    await call.message.answer(text="✅ Profil muvaffaqiyatli o'zgartirildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text='no', state=UpdateParentProfileState.phone_number)
async def cancel_changes_parent_profile_function(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Profil o'zgarishini rad etdingiz", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=UpdateParentProfileState.phone_number, text="Keyingi 🔜")
@dp.message_handler(state=UpdateParentProfileState.phone_number)
async def get_parent_phone_number_function(message: types.Message, state: FSMContext):
    phone_number = message.text
    if phone_number != "Keyingi 🔜":
        await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    child_first_name = data.get("child_first_name")
    child_last_name = data.get("child_last_name")
    phone_number = data.get("phone_number")

    text = (f"🔄 Profilingiz o'zgarishlardan so'ng quyidagicha bo'ladi 👇\n"
            f"🧑‍💼 Farzandingizning ismi: {child_first_name}\n"
            f"👤 Farzandingizning familiyasi: {child_last_name}\n"
            f"📞 Telefon raqamingiz: {phone_number}\n")
    await message.answer(text=text)
    await message.answer(text="Saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)

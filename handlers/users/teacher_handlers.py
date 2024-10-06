from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.all_groups import my_groups_default_keyboard
from keyboards.default.all_students import all_students_in_group
from keyboards.default.all_users import all_users_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.group_actions import group_actions_for_teachers
from keyboards.default.menu_keyboards import back_to_menu, go_back_default_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from loader import dp, db, bot
from states.groups import GetGroupState, AddStudentToGroupStateForTeacher, \
    DeleteStudentFromGroupStateForTeacher


@dp.message_handler(text="🔙 Orqaga", state=[GetGroupState.group_id])
@dp.message_handler(text="👥 Guruhlarim", state="*")
async def my_groups(message: types.Message, state: FSMContext):
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
        if user_role != 'teacher':
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            teacher_profiles = await db.select_teacher_profiles(user_id=user['id'])
            teacher_id = teacher_profiles[0]['id']
            groups = await db.select_groups(teacher_id=teacher_id)
            if not groups:
                await message.answer(text="🚫 Sizda hali guruh mavjud emas", reply_markup=back_to_menu)
                return
            markup = await my_groups_default_keyboard(teacher_id=teacher_id)
            await message.answer(text="Guruhlardan birini tanlang 👇", reply_markup=markup)
            await GetGroupState.group_id.set()


# for adding student
@dp.message_handler(state=GetGroupState.group_id, text="➕ O'quvchi qo'shish")
async def start_adding_student_to_group(message: types.Message, state: FSMContext):
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
            await state.finish()

            markup = await all_users_default_keyboard()
            await message.answer(text="👥 Guruhga o'quvchi qo'shish uchun foydalanuvchilardan birini tanlang 👇",
                                 reply_markup=markup)

            await AddStudentToGroupStateForTeacher.user_id.set()
            await state.update_data(group_id=group_id)


@dp.message_handler(state=GetGroupState.group_id, text="➖ O'quvchini o'chirish")
async def start_deleting_student_from_group(message: types.Message, state: FSMContext):
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
            await state.finish()

            markup = await all_students_in_group(group_id=group_id)
            await message.answer(text="O'chirilishi kerak bo'lgan o'quvchini tanlang 👇", reply_markup=markup)
            await DeleteStudentFromGroupStateForTeacher.parent_id.set()
            await state.update_data(group_id=group_id)


@dp.callback_query_handler(state=AddStudentToGroupStateForTeacher.user_id, text='yes')
async def confirm_adding_student(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    group_id = data.get('group_id')
    user_id = data.get('user_id')

    group = await db.select_group(group_id=group_id)

    user = await db.update_user(
        user_id=user_id,
        role='parent'
    )

    parent = await db.create_parent_profile(
        user_id=user_id,
        group_id=group_id
    )
    await state.update_data(parent_id=parent['id'])
    await call.message.answer(text=f"✅ {user['full_name']} {group['name']}ga muvaffaqiyatli qo'shildi\n"
                                   f"✍️ Endi bu o'quvchi uchun ism kiriting:", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await AddStudentToGroupStateForTeacher.child_first_name.set()


@dp.callback_query_handler(state=AddStudentToGroupStateForTeacher.user_id, text='no')
async def cancel_adding_student(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ O'quvchi qo'shish bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=AddStudentToGroupStateForTeacher.child_last_name, text="🔙 Orqaga")
async def get_child_first_name(message: types.Message, state: FSMContext):
    await message.answer(text="✍️ O'quvchining ismini kiriting:", reply_markup=back_to_menu)
    await AddStudentToGroupStateForTeacher.child_first_name.set()


@dp.message_handler(state=AddStudentToGroupStateForTeacher.child_first_name)
async def get_child_first_name(message: types.Message, state: FSMContext):
    first_name = message.text
    await state.update_data(child_first_name=first_name)
    await message.answer(text="✍️ O'quvchining familiyasini kiriting:", reply_markup=go_back_default_keyboard)
    await AddStudentToGroupStateForTeacher.child_last_name.set()


@dp.callback_query_handler(state=AddStudentToGroupStateForTeacher.child_last_name, text='yes')
async def change_child_information(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    first_name = data.get('child_first_name')
    last_name = data.get('child_last_name')
    parent_id = data.get('parent_id')
    parent_profile = await db.update_parent_profile(
        profile_id=parent_id,
        child_first_name=first_name,
        child_last_name=last_name,
    )
    await call.message.answer(text="✅ O'quvchi ma'lumotlari saqlandi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=AddStudentToGroupStateForTeacher.child_last_name, text='no')
async def cancel_change_child_information(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Saqlash rad etildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=AddStudentToGroupStateForTeacher.child_last_name)
async def get_child_last_name(message: types.Message, state: FSMContext):
    last_name = message.text
    data = await state.get_data()
    first_name = data.get('child_first_name')
    await state.update_data(child_last_name=last_name)
    text = (f"O'quvchi ism-familiyasi 👇\n"
            f"Ism: {first_name}\n"
            f"Familiya: {last_name}")
    await message.answer(text=text)
    await message.answer(text="O'quvchi ma'lumotlarini saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)


# this is except from other codes: for getting group id
@dp.message_handler(state=[
    AddStudentToGroupStateForTeacher.user_id,
    DeleteStudentFromGroupStateForTeacher.parent_id,
],
    text="🔙 Orqaga")
@dp.message_handler(state=[GetGroupState.group_id])
async def get_group_id(message: types.Message, state: FSMContext):
    group_name = message.text
    if group_name != "🔙 Orqaga":
        groups = await db.select_groups(name=group_name)
        if not groups:
            await message.answer(text="⚠️ Bu guruh allaqachon o'chirib yuborilgan",
                                 reply_markup=go_back_default_keyboard)
            return
        group_id = groups[0]['id']
        await state.update_data(group_id=group_id)
        data = await state.get_data()
    else:
        await GetGroupState.group_id.set()
    await message.answer(text="Amallardan birini tanlang 👇", reply_markup=group_actions_for_teachers)


@dp.message_handler(state=AddStudentToGroupStateForTeacher.user_id)
async def get_user_id_for_add_student_to_group(message: types.Message, state: FSMContext):
    full_name = message.text
    first_name = full_name.split()[0]
    last_name = full_name.split()[1]
    users = await db.select_users(full_name=full_name)
    if not users:
        await message.answer(text="⚠️ Bu foydalanuvchi allaqachon o'chirib yuborilgan",
                             reply_markup=go_back_default_keyboard)
        return
    user_id = users[0]['id']

    data = await state.get_data()
    group_id = data.get('group_id')
    group = await db.select_group(group_id=group_id)
    group_name = group['name']

    await state.update_data(user_id=user_id)
    await message.answer(text=f"Haqiqatdan ham {full_name}ni {group_name}ga qo'shmoqchimisiz?",
                         reply_markup=confirm_keyboard)


# for delete students from group for teacher
@dp.callback_query_handler(state=DeleteStudentFromGroupStateForTeacher.parent_id, text="yes")
async def delete_student_from_group_final(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    group_id = data.get('group_id')
    parent_id = data.get('parent_id')

    parent_profile = await db.select_parent_profile(profile_id=parent_id)
    user_id = parent_profile['user_id']

    await db.delete_parent_profile(
        profile_id=parent_id,
    )

    user = await db.update_user(
        user_id=user_id,
        role='user'
    )
    await call.message.answer(text="✅ Foydalanuvchi guruhdan chiqarib tashlandi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=DeleteStudentFromGroupStateForTeacher.parent_id, text="no")
async def cancel_removing_student(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Amaliyot bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=DeleteStudentFromGroupStateForTeacher.parent_id)
async def get_student(message: types.Message, state: FSMContext):
    student_full_name = message.text
    first_name = student_full_name.split()[0]
    last_name = student_full_name.split()[1]
    parent_profiles = await db.select_parent_profiles(child_first_name=first_name, child_last_name=last_name)
    if not parent_profiles:
        await message.answer(text="Bu o'quvchi allaqachon guruhdan chiqarib yuborilgan",
                             reply_markup=go_back_default_keyboard)
        return
    parent_profile_id = parent_profiles[0]['id']
    await state.update_data(parent_id=parent_profile_id)
    data = await state.get_data()
    group_id = data.get('group_id')
    group = await db.select_group(group_id=group_id)
    await message.answer(text=f"Haqiqatdan ham {student_full_name} ni {group['name']}dan chiqarib tashlamoqchimisiz?",
                         reply_markup=confirm_keyboard)

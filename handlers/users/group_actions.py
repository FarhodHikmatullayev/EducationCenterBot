from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.default.all_groups import all_groups_default_keyboard
from keyboards.default.all_students import all_students_in_group
from keyboards.default.all_teachers import all_teachers_default_keyboard, all_teachers_and_next_default_keyboard
from keyboards.default.change_profile_keyboards import next_change_default_keyboard
from keyboards.default.confirm_actions_for_group import delete_group_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.group_actions import group_actions_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu, go_back_default_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from loader import dp, db, bot
from states.groups import DeleteGroupState, CreateGroupState, UpdateGroupState, RemoveStudentFromGroupState


# for delete
@dp.message_handler(text="🗑️ O'chirish", state=DeleteGroupState.group_id)
async def delete_group_final_function(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group_id = data.get("group_id")
    group = await db.select_group(group_id=group_id)
    if group:
        parent_profiles = await db.select_parent_profiles(group_id=group_id)
        for parent_profile in parent_profiles:
            user_id = parent_profile['user_id']
            await db.update_user(user_id=user_id, role='user')
            await db.delete_parent_profile(profile_id=parent_profile["id"])

        await db.delete_group(group_id=group_id)
        await message.answer(text="📣 Guruh muvaffaqiyatli o'chirildi ✅", reply_markup=back_to_menu)
    else:
        await message.answer(text="📢 Bu guruh allaqachon o'chirilgan", reply_markup=back_to_menu)
    await state.finish()


@dp.message_handler(text="🗑️ Guruhni o'chirish", state="*")
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
            markup = await all_groups_default_keyboard()
            await message.answer(text="O'chirmoqchi bo'lgan guruhni tanlang 👇", reply_markup=markup)
            await DeleteGroupState.group_id.set()


# afasdfasfsdfasd
@dp.message_handler(text="🔙 Orqaga", state=DeleteGroupState.group_id)
async def back_to_actions(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Kerakli amalni tanlang 👇", reply_markup=group_actions_default_keyboard)


@dp.message_handler(text="🔙 Guruhlarga qaytish", state=DeleteGroupState.group_id, user_id=ADMINS)
async def back_to_groups_list(message: types.Message, state: FSMContext):
    markup = await all_groups_default_keyboard()
    await message.answer(text="O'chirmoqchi bo'lgan guruhni tanlang 👇", reply_markup=markup)
    await DeleteGroupState.group_id.set()


# aasdfadfasd

@dp.message_handler(state=DeleteGroupState.group_id)
async def delete_teacher(message: types.Message, state: FSMContext):
    group_name = message.text

    groups = await db.select_groups(name=group_name)
    group = groups[0]
    group_id = group['id']
    teacher_id = group['teacher_id']
    teacher_profiles = await db.select_teacher_profiles(id=teacher_id)
    if teacher_profiles:
        teacher_profile = teacher_profiles[0]
        teacher_full_name = f"{teacher_profile['first_name']} {teacher_profile['last_name']}"
    else:
        teacher_full_name = "Hali o'qituvchi ta'yinlanmagan"

    parent_profiles = await db.select_parent_profiles(group_id=group_id)
    if parent_profiles:
        count_students = len(parent_profiles)
    else:
        count_students = 0

    await state.update_data(
        name=group_name,
        group_id=group_id
    )
    text = (f"🏫 Guruh nomi: {group_name}\n"
            f"👨‍🏫 Guruh o'qituvchisi: {teacher_full_name}\n"
            f"👩‍🎓 Guruh o'quvchilari soni: {count_students}\n")
    await message.answer(text=text)
    await message.answer(text="💬 Guruhni o'chirasizmi?\n"
                              "O'chirish tumasini bosing 👇", reply_markup=delete_group_default_keyboard)


# for create
@dp.message_handler(state=CreateGroupState.teacher_id, text="🔙 Orqaga")
@dp.message_handler(text="➕ Yangi guruh yaratish", state='*')
async def start_creating_group(message: types.Message, state: FSMContext):
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
            await message.answer(text="🆕 Yangi guruh uchun nom kiriting:", reply_markup=go_back_default_keyboard)
            await CreateGroupState.name.set()


@dp.message_handler(state=CreateGroupState.name)
async def get_group_name(message: types.Message, state: FSMContext):
    group_name = message.text
    await state.update_data(name=group_name)
    markup = await all_teachers_default_keyboard()
    await message.answer(text="Guruh uchun o'qituvchi tanlang 👇", reply_markup=markup)
    await CreateGroupState.teacher_id.set()


@dp.callback_query_handler(state=CreateGroupState.teacher_id, text="yes")
async def save_group(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    teacher_id = data.get('teacher_id')
    group_name = data.get('name')
    group = await db.create_group(
        name=group_name,
        teacher_id=teacher_id
    )
    await call.message.answer(text="✅ Guruh saqlandi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=CreateGroupState.teacher_id, text="no")
async def cancel_saving_group(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Saqlash rad etildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=CreateGroupState.teacher_id)
async def get_teacher_name(message: types.Message, state: FSMContext):
    teacher_full_name = message.text
    teacher_first_name = teacher_full_name.split()[0]
    teacher_last_name = teacher_full_name.split()[1]
    teachers = await db.select_teacher_profiles(first_name=teacher_first_name, last_name=teacher_last_name)
    if not teachers:
        await message.answer(text="⚠️ Bu o'qituvchi o'chirib yuborilgan", reply_markup=go_back_default_keyboard)
        return
    teacher = teachers[0]
    await state.update_data(teacher_id=teacher['id'])
    data = await state.get_data()
    group_name = data.get('name')
    await message.answer(text=f"📋 Guruh quyidagicha bo'ladi 👇\n"
                              f"🏫 Guruh nomi: {group_name}\n"
                              f"👩‍🏫 Guruh o'qituvchisi: {teacher_full_name}\n")
    await message.answer(text="📥 Guruhni saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)


# for update
@dp.message_handler(text="✏️ Guruhni o'zgartirish", state="*")
async def start_editing_group(message: types.Message, state: FSMContext):
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
            markup = await all_groups_default_keyboard()
            await message.answer(text="O'zgartirmoqchi bo'lgan guruhni tanlang 👇", reply_markup=markup)
            await UpdateGroupState.group_id.set()


@dp.message_handler(state=UpdateGroupState.group_id)
async def get_group_id(message: types.Message, state: FSMContext):
    group_name = message.text
    groups = await db.select_groups(name=group_name)
    if not groups:
        await message.answer(text="⚠️ Bu guruh allaqachon o'chirib yuborilgan", reply_markup=go_back_default_keyboard)
        return
    group = groups[0]
    group_id = group['id']
    await state.update_data(group_id=group_id, name=group_name)
    await message.answer(text="📝 Agar guruh nomini o'zgartirmoqchi bo'lsangiz, \n"
                              "🔤 Yangi nom kiriting,\n"
                              "❌ Aks holda 'Keyingi' tugmasini bosing 👇", reply_markup=next_change_default_keyboard)
    await UpdateGroupState.name.set()


@dp.message_handler(state=UpdateGroupState.name, text="Keyingi 🔜")
@dp.message_handler(state=UpdateGroupState.name)
async def get_group_name(message: types.Message, state: FSMContext):
    group_name = message.text
    if group_name != "Keyingi 🔜":
        await state.update_data(name=group_name)
    markup = await all_teachers_and_next_default_keyboard()
    await message.answer(
        text="👨‍🏫 Guruh o'qituvchisini o'zgartirmoqchi bo'lsangiz, \n" \
             "📋 o'qituvchilardan birini tanlang, \n" \
             "❌ aks holda 'Keyingi' tugmasini bosing 👇", reply_markup=markup)
    await UpdateGroupState.teacher_id.set()


@dp.callback_query_handler(state=UpdateGroupState.teacher_id, text="yes")
async def update_group(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    teacher_id = data.get('teacher_id')
    group_name = data.get('name')
    group_id = data.get('group_id')
    group = await db.update_group(
        group_id=group_id,
        name=group_name,
        teacher_id=teacher_id
    )
    await call.message.answer(text="✅ Guruh saqlandi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=UpdateGroupState.teacher_id, text="no")
async def cancel_updating_group(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Saqlash rad etildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=UpdateGroupState.teacher_id, text="Keyingi 🔜")
@dp.message_handler(state=UpdateGroupState.teacher_id)
async def get_teacher_id(message: types.Message, state: FSMContext):
    teacher_full_name = message.text
    if teacher_full_name != "Keyingi 🔜":
        teacher_first_name = teacher_full_name.split()[0]
        teacher_last_name = teacher_full_name.split()[1]
        teachers = await db.select_teacher_profiles(first_name=teacher_first_name, last_name=teacher_last_name)
        if not teachers:
            await message.answer(text="⚠️ Bu o'qituvchi allaqachon o'chirib yuborilgan", reply_markup=back_to_menu)
            return
        teacher = teachers[0]
        teacher_id = teacher['id']
        await state.update_data(teacher_id=teacher_id)
    data = await state.get_data()
    group_name = data.get('name')
    teacher_id = data.get('teacher_id')
    if not teacher_id:
        teacher_full_name = "Hali kiritilmagan"
    await message.answer(text=f"📋 Guruh quyidagicha bo'ladi 👇\n"
                              f"🏫 Guruh nomi: {group_name}\n"
                              f"👩‍🏫 Guruh o'qituvchisi: {teacher_full_name}\n")
    await message.answer(text="📥 Guruhni saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)


# for delete student
@dp.message_handler(state=RemoveStudentFromGroupState.student_id, text="🔙 Orqaga")
@dp.message_handler(text="➖ Guruhdan o'quvchini o'chirish", state="*")
async def start_deleting_student_from_group(message: types.Message, state: FSMContext):
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
            markup = await all_groups_default_keyboard()
            await message.answer(text="❓ Qaysi guruhdan o'quvchi o'chirmoqchisiz?\n"
                                      "🔍 Guruhlardan birini tanlang 👇", reply_markup=markup)
            await RemoveStudentFromGroupState.group_id.set()


@dp.message_handler(state=RemoveStudentFromGroupState.group_id)
async def get_group_id(message: types.Message, state: FSMContext):
    group_name = message.text
    groups = await db.select_groups(name=group_name)
    if not groups:
        await message.answer(text="⚠️ Bu guruh allaqachon o'chirib tashlangan", reply_markup=go_back_default_keyboard)
        return
    group_id = groups[0]['id']
    await state.update_data(group_id=group_id)
    markup = await all_students_in_group(group_id=group_id)
    await message.answer(text="❓ Qaysi o'quvchini o'chirmoqchisiz?\n"
                              "👤 O'quvchilardan birini tanlang 👇",
                         reply_markup=markup)
    await RemoveStudentFromGroupState.student_id.set()


@dp.callback_query_handler(text='yes', state=RemoveStudentFromGroupState.student_id)
async def remove_student(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    group_id = data.get('group_id')
    student_id = data.get('student_id')
    parent_profile = await db.select_parent_profile(profile_id=student_id)
    user_id = parent_profile['user_id']

    await db.delete_parent_profile(profile_id=student_id)
    await db.update_user(
        user_id=user_id,
        role='user'
    )
    await call.message.answer(text="✅ O'quvchi guruhdan olib tashlandi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text='no', state=RemoveStudentFromGroupState.student_id)
async def cancel_removing_student(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ O'quvchini chiqarib yuborish bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=RemoveStudentFromGroupState.student_id)
async def get_student_id(message: types.Message, state: FSMContext):
    stunt_full_name = message.text
    first_name = stunt_full_name.split()[0]
    last_name = stunt_full_name.split()[1]
    parent_profiles = await db.select_parent_profiles(child_first_name=first_name, child_last_name=last_name)
    if not parent_profiles:
        await message.answer(text="⚠️ Bu o'quvchi allaqachon guruhdan o'chirib yuborilgan",
                             reply_markup=go_back_default_keyboard)
        return
    parent_profile_id = parent_profiles[0]['id']
    await state.update_data(student_id=parent_profile_id)
    await message.answer(text=f"Haqiqatdan ham {stunt_full_name}ni guruhdan chiqarib tashlamoqchimisiz?\n",
                         reply_markup=confirm_keyboard)

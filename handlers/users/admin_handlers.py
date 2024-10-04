from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.group_actions import group_actions_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu
from keyboards.default.profiles import change_profile_default_keyboard
from keyboards.default.teacher_actions import teacher_actions_default_keyboard
from loader import dp, db
from states.groups import CreateGroupState, UpdateGroupState, RemoveStudentFromGroupState
from states.teachers import CreateTeacherState, UpdateTeacherState


@dp.message_handler(text="🔙 Orqaga", state=[CreateTeacherState.first_name, UpdateTeacherState.teacher_id])
@dp.message_handler(text="👩‍🏫 O'qituvchilar", state="*")
async def get_actions_for_teachers(message: types.Message, state: FSMContext):
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
        if user_role != "admin":
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            await message.answer(text="Kerakli amalni tanlang 👇", reply_markup=teacher_actions_default_keyboard)


@dp.message_handler(state=[CreateGroupState.name, UpdateGroupState.group_id, RemoveStudentFromGroupState.group_id],
                    text="🔙 Orqaga")
@dp.message_handler(text="👥 Guruhlar", state="*")
async def get_actions_for_groups(message: types.Message, state: FSMContext):
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
        if user_role != "admin":
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            await message.answer(text="Kerakli amalni tanlang 👇", reply_markup=group_actions_default_keyboard)


@dp.message_handler(text="👤 Mening Profilim", state="*")
async def go_to_my_profile(message: types.Message, state: FSMContext):
    print(1)
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
        full_name = user['full_name']
        phone_number = user['phone']
        first_name = full_name.split()[0]
        last_name = full_name.split()[1]
        user_id = user['id']
        if user_role == "admin":
            text = (f"📋 Sizning ma'lumotlaringiz 👇\n"
                    f"🧑‍💼 Ismingiz: {first_name}\n"
                    f"👤 Familiyangiz: {last_name}\n"
                    f"📞 Telefon raqamingiz: {phone_number}\n"
                    f"🔑 Rol: ADMIN\n")
        elif user_role == "teacher":
            teachers = await db.select_teacher_profiles(user_id=user_id)
            teacher = teachers[0]
            teacher_id = teacher['id']
            experience = teacher['experience']
            birth_year = teacher['birth_year']
            this_year = datetime.now().year
            age = this_year - birth_year
            groups = await db.select_groups(teacher_id=teacher_id)
            text = (f"📋 Sizning ma'lumotlaringiz 👇\n"
                    f"🧑‍💼 Ismingiz: {first_name}\n"
                    f"👤 Familiyangiz: {last_name}\n"
                    f"📞 Telefon raqamingiz: {phone_number}\n"
                    f"🎂 Yoshingiz: {age} \n"
                    f"💼 Ish stajingiz: {experience} yil\n")
            if groups:
                tr = 1
                text += f"📚 Guruhlaringiz:\n"
                for group in groups:
                    text += f"\t{tr}. {group['name']}\n"
        elif user_role == "parent":
            parent = await db.select_parent_profiles(user_id=user_id)
            parent = parent[0]
            parent_id = parent['id']
            child_first_name = parent['child_first_name']
            child_last_name = parent['child_last_name']
            group_id = parent['group_id']
            groups = await db.select_groups(id=group_id)
            if groups:
                group = groups[0]
                group_name = group['name']
                teacher_id = group['teacher_id']
                teachers = await db.select_teacher_profiles(id=teacher_id)
                teacher = teachers[0]
                teacher_user_id = teacher['user_id']
                users = await db.select_users(id=teacher_user_id)
                user = users[0]
                teacher_full_name = user['full_name']
            else:
                teacher_full_name = "Hali sizga o'qituvchi belgilanmagan"
                group_name = "Hali siz guruhlardan biriga qo'shilmagansiz"

            text = (f"📄 Sizning ma'lumotlaringiz 👇\n"
                    f"👶 Farzanderingiz ismi: {child_first_name}\n"
                    f"👦 Farzandingiz familiyasi: {child_last_name}\n"
                    f"🏫 Farzandingiz guruhi: {group_name}\n"
                    f"👩‍🏫 Farzandingiz o'qituvchisi: {teacher_full_name}\n"
                    f"📞 Telefon raqamingiz: {phone_number}\n")
        else:
            text = "❌ Sizda hali profil mavjud emas"
            await message.reply(text=text)
            return
        await message.answer(text=text, reply_markup=change_profile_default_keyboard)

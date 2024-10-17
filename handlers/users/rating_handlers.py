
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.all_groups import all_groups_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu, go_back_default_keyboard
from keyboards.default.my_children_keyboard import my_children_default_keyboard
from loader import dp, db, bot
from states.groups import GetGroupState, GetGroupStateForAdmin
from states.profile_states import GetProfileState, GetProfileStateForRating


# this is for teachers
@dp.message_handler(state=GetGroupState.group_id, text="📊 Guruh o'quvchilari reytingi")
async def get_rates_of_the_group(message: types.Message, state: FSMContext):
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
            parent_profiles = await db.select_parent_profiles(group_id=group_id)
            if not parent_profiles:
                await message.answer(text="🚫 Bu guruhda hali o'quvchilar mavjud emas",
                                     reply_markup=go_back_default_keyboard)
                return
            sum_of_marks_dict = dict()
            for parent_profile in parent_profiles:
                student_full_name = f"{parent_profile['child_first_name']} {parent_profile['child_last_name']}"
                sum_of_marks_dict[student_full_name] = 0
                monthly_marks = await db.select_last_month_marks(student_id=parent_profile['id'])
                for mark in monthly_marks:
                    sum_of_marks_dict[student_full_name] += mark['kayfiyat']
                    sum_of_marks_dict[student_full_name] += mark['tartib']
                    sum_of_marks_dict[student_full_name] += mark['faollik']
                    sum_of_marks_dict[student_full_name] += mark['vaqtida_kelish']
                    sum_of_marks_dict[student_full_name] += mark['dars_qoldirmaslik']
                    sum_of_marks_dict[student_full_name] += mark['vazifa_bajarilganligi']
                    sum_of_marks_dict[student_full_name] += mark['darsni_ozlashtirish']
            sorted_data = sorted(sum_of_marks_dict.items(), key=lambda x: x[1], reverse=True)

            # Natijani shakllantirish
            result_str = []
            for i, (name, score) in enumerate(sorted_data):
                if i == 0:
                    result_str.append(f"🥇 {name}: {score}")  # Birinchi o'rin
                elif i == 1:
                    result_str.append(f"🥈 {name}: {score}")  # Ikkinchi o'rin
                elif i == 2:
                    result_str.append(f"🥉 {name}: {score}")  # Uchinchi o'rin
                else:
                    result_str.append(f"{i + 1}. {name}: {score}")  # Boshqa o'rinlar

            # Result text
            text = "📊 Oxirgi bir oylik natijalar:\n"
            text += "\n".join(result_str)
            await message.answer(text=text, reply_markup=go_back_default_keyboard)


# this is for admins
@dp.message_handler(state="*", text="📊 Guruh o'quvchilari reytingini ko'rish")
async def get_rates_of_the_group_for_admin(message: types.Message, state: FSMContext):
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
            await message.answer(text="Reytingni ko'rish uchun guruhlardan birini tanlang 👇", reply_markup=markup)
            await GetGroupStateForAdmin.group_id.set()


@dp.message_handler(state=GetGroupStateForAdmin.group_id)
async def get_result_rate_for_admin(message: types.Message, state: FSMContext):
    group_name = message.text
    groups = await db.select_groups(name=group_name)
    if not groups:
        await message.answer(text="Bu guruh allaqachon o'chirib yuborilgan", reply_markup=go_back_default_keyboard)
        return
    group = groups[0]
    group_id = group['id']
    teacher_id = group['teacher_id']
    teacher_profile = await db.select_teacher_profile(profile_id=teacher_id)
    if teacher_profile:
        teacher_full_name = f"{teacher_profile['first_name']} {teacher_profile['last_name']}"
    else:
        teacher_full_name = "Hali ta'yinlanmagan"
    await state.update_data(group_id=group_id, teacher_id=teacher_id)
    data = await state.get_data()

    group_id = data.get('group_id')
    parent_profiles = await db.select_parent_profiles(group_id=group_id)
    if not parent_profiles:
        await message.answer(text="🚫 Bu guruhda hali o'quvchilar mavjud emas",
                             reply_markup=go_back_default_keyboard)
        return
    sum_of_marks_dict = dict()
    for parent_profile in parent_profiles:
        student_full_name = f"{parent_profile['child_first_name']} {parent_profile['child_last_name']}"
        sum_of_marks_dict[student_full_name] = 0
        monthly_marks = await db.select_last_month_marks(student_id=parent_profile['id'])
        for mark in monthly_marks:
            sum_of_marks_dict[student_full_name] += mark['kayfiyat']
            sum_of_marks_dict[student_full_name] += mark['tartib']
            sum_of_marks_dict[student_full_name] += mark['faollik']
            sum_of_marks_dict[student_full_name] += mark['vaqtida_kelish']
            sum_of_marks_dict[student_full_name] += mark['dars_qoldirmaslik']
            sum_of_marks_dict[student_full_name] += mark['vazifa_bajarilganligi']
            sum_of_marks_dict[student_full_name] += mark['darsni_ozlashtirish']
    sorted_data = sorted(sum_of_marks_dict.items(), key=lambda x: x[1], reverse=True)

    # Natijani shakllantirish
    result_str = []
    for i, (name, score) in enumerate(sorted_data):
        if i == 0:
            result_str.append(f"🥇 {name}: {score}")  # Birinchi o'rin
        elif i == 1:
            result_str.append(f"🥈 {name}: {score}")  # Ikkinchi o'rin
        elif i == 2:
            result_str.append(f"🥉 {name}: {score}")  # Uchinchi o'rin
        else:
            result_str.append(f"{i + 1}. {name}: {score}")  # Boshqa o'rinlar

    # Result text
    text = "📊 Oxirgi bir oylik natijalar:\n"
    text += "\n".join(result_str)
    text += f"\nGuruh o'qituvchisi: {teacher_full_name}"
    await message.answer(text=text, reply_markup=go_back_default_keyboard)


# for parents
@dp.message_handler(state="*", text="📊 Baholar reytingi")
async def get_rating_for_parents(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.answer(text="🚫 Sizda botdan foydalanish uchun ruxsat mavjud emas,\n"
                                  "📝 Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak 👇",
                             reply_markup=back_to_menu)
    else:
        user = users[0]
        user_role = user['role']
        if user_role != 'parent':
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            parent_profiles = await db.select_parent_profiles(user_id=user['id'])
            if len(parent_profiles) == 1:
                parent_profile = parent_profiles[0]
                my_id = parent_profile['id']
                group_id = parent_profile['group_id']
                my_name = f"{parent_profile['child_first_name']} {parent_profile['child_last_name']}"

                parent_profiles = await db.select_parent_profiles(group_id=group_id)
                sum_of_marks_dict = dict()
                for parent_profile in parent_profiles:
                    student_full_name = f"{parent_profile['child_first_name']} {parent_profile['child_last_name']}"
                    sum_of_marks_dict[student_full_name] = 0
                    monthly_marks = await db.select_last_month_marks(student_id=parent_profile['id'])
                    for mark in monthly_marks:
                        sum_of_marks_dict[student_full_name] += mark['kayfiyat']
                        sum_of_marks_dict[student_full_name] += mark['tartib']
                        sum_of_marks_dict[student_full_name] += mark['faollik']
                        sum_of_marks_dict[student_full_name] += mark['vaqtida_kelish']
                        sum_of_marks_dict[student_full_name] += mark['dars_qoldirmaslik']
                        sum_of_marks_dict[student_full_name] += mark['vazifa_bajarilganligi']
                        sum_of_marks_dict[student_full_name] += mark['darsni_ozlashtirish']
                sorted_data = sorted(sum_of_marks_dict.items(), key=lambda x: x[1], reverse=True)

                # Natijani shakllantirish
                result_str = []
                icon_list = ["👤", "🙈", "🎭", "🕵️‍♂️", "🦸‍♀️"]
                for i, (name, score) in enumerate(sorted_data):
                    if name != my_name:
                        name = icon_list[i % len(icon_list)] + " (Anonim)"

                    if i == 0:
                        result_str.append(f"🥇 {name}: {score}")  # Birinchi o'rin
                    elif i == 1:
                        result_str.append(f"🥈 {name}: {score}")  # Ikkinchi o'rin
                    elif i == 2:
                        result_str.append(f"🥉 {name}: {score}")  # Uchinchi o'rin
                    else:
                        result_str.append(f"{i + 1}. {name}: {score}")  # Boshqa o'rinlar

                # Result text
                text = "📊 Oxirgi bir oylik natijalar:\n"
                text += "\n".join(result_str)
                await message.answer(text=text, reply_markup=back_to_menu)
            else:
                markup = await my_children_default_keyboard(user_id=user['id'])
                await message.answer(text="Farzandlaringizdan birini tanlang 👇", reply_markup=markup)
                await GetProfileStateForRating.profile_id.set()


@dp.message_handler(state=GetProfileStateForRating.profile_id)
async def get_profile_id(message: types.Message, state: FSMContext):
    child_full_name = message.text
    child_first_name = child_full_name.split()[0]
    child_last_name = child_full_name.split()[1]
    parent_profiles = await db.select_parent_profiles(child_first_name=child_first_name,
                                                      child_last_name=child_last_name)
    if not parent_profiles:
        await message.answer(text="⚠️ Farzandingiz guruhdan o'chirib yuborilgan", reply_markup=back_to_menu)
        return
    parent_id = parent_profiles[0]['id']
    await state.update_data(profile_id=parent_id)
    parent_profile = parent_profiles[0]

    group_id = parent_profile['group_id']
    my_name = f"{parent_profile['child_first_name']} {parent_profile['child_last_name']}"

    parent_profiles = await db.select_parent_profiles(group_id=group_id)
    sum_of_marks_dict = dict()
    for parent_profile in parent_profiles:
        student_full_name = f"{parent_profile['child_first_name']} {parent_profile['child_last_name']}"
        sum_of_marks_dict[student_full_name] = 0
        monthly_marks = await db.select_last_month_marks(student_id=parent_profile['id'])
        for mark in monthly_marks:
            sum_of_marks_dict[student_full_name] += mark['kayfiyat']
            sum_of_marks_dict[student_full_name] += mark['tartib']
            sum_of_marks_dict[student_full_name] += mark['faollik']
            sum_of_marks_dict[student_full_name] += mark['vaqtida_kelish']
            sum_of_marks_dict[student_full_name] += mark['dars_qoldirmaslik']
            sum_of_marks_dict[student_full_name] += mark['vazifa_bajarilganligi']
            sum_of_marks_dict[student_full_name] += mark['darsni_ozlashtirish']
    sorted_data = sorted(sum_of_marks_dict.items(), key=lambda x: x[1], reverse=True)

    # Natijani shakllantirish
    result_str = []
    icon_list = ["👤", "🙈", "🎭", "🕵️‍♂️", "🦸‍♀️"]
    for i, (name, score) in enumerate(sorted_data):
        if name != my_name:
            name = icon_list[i % len(icon_list)] + " (Anonim)"

        if i == 0:
            result_str.append(f"🥇 {name}: {score}")  # Birinchi o'rin
        elif i == 1:
            result_str.append(f"🥈 {name}: {score}")  # Ikkinchi o'rin
        elif i == 2:
            result_str.append(f"🥉 {name}: {score}")  # Uchinchi o'rin
        else:
            result_str.append(f"{i + 1}. {name}: {score}")  # Boshqa o'rinlar

    # Result text
    text = "📊 Oxirgi bir oylik natijalar:\n"
    text += "\n".join(result_str)
    await message.answer(text=text, reply_markup=back_to_menu)
    await state.finish()

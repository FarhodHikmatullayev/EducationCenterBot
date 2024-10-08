from datetime import datetime
from idlelib.window import add_windows_to_menu

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import GROUP_CHAT_ID
from keyboards.default.contact_keyboards import contact_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu, go_back_default_keyboard
from keyboards.default.my_children_keyboard import my_children_default_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from loader import dp, db, bot
from states.idea_states import IdeaStates, Objection, Incentive
from states.profile_states import GetProfileState


@dp.message_handler(text="🔙 Orqaga", state=[Incentive.text, Objection.text, IdeaStates.text])
@dp.message_handler(text="📞 O'qituvchi bilan bog'lanish", state="*")
async def contact_with_teacher(message: types.Message, state: FSMContext):
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
        if user_role != 'parent':
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            user_id = user['id']
            parent_profiles = await db.select_parent_profiles(user_id=user_id)
            if len(parent_profiles) == 1:
                parent_profile = parent_profiles[0]
                await GetProfileState.profile_id.set()
                await state.update_data(profile_id=parent_profile['id'])
                print('profile_id', parent_profile['id'])
                group_id = parent_profile['group_id']
                group = await db.select_group(group_id=group_id)
                teacher_id = group['teacher_id']
                teacher_profile = await db.select_teacher_profile(profile_id=teacher_id)
                teacher_user_id = teacher_profile['user_id']
                teacher_user = await db.select_user(user_id=teacher_user_id)
                experience = teacher_profile['experience']
                experience = experience if experience else "Hali kiritilmagan"
                age = (datetime.now().year - teacher_profile['birth_year']) if teacher_profile[
                    'birth_year'] else "Hali kiritilmagan"
                text = (f"📚 O'qituvchi ma'lumotlari:\n"
                        f"🧑‍💼 Ismi: {teacher_profile['first_name']}\n"
                        f"👤 Familiyasi: {teacher_profile['last_name']}\n"
                        f"📅 Yoshi: {age}\n"
                        f"💼 Ish staji: {experience}\n"
                        f"📞 Tel: {teacher_user['phone']}\n")

                await message.answer(text=text)
                await message.answer(
                    text="📝O'qituvchiga quyidagi bo'limlardan birini tanlab, o'z xabaringizni qoldiring 👇",
                    reply_markup=contact_default_keyboard
                )
            else:
                markup = await my_children_default_keyboard(user_id=user_id)
                await message.answer(text="Farzandlaringizdan birini tanlang 👇", reply_markup=markup)
                await GetProfileState.profile_id.set()


@dp.message_handler(text="📩 Taklif yuborish", state=GetProfileState.profile_id)
async def start_sending_idea(message: types.Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.answer(text="🚫 Sizda botdan foydalanish uchun ruxsat mavjud emas,\n"
                                  "📝 Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak 👇",
                             reply_markup=go_registration_default_keyboard)
    else:
        user = users[0]
        user_role = user['role']
        if user_role != 'parent':
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            await message.answer(text="✍️ Yubormoqchi bo'lgan taklifingizni yozing:",
                                 reply_markup=go_back_default_keyboard)
            data = await state.get_data()
            profile_id = data.get('profile_id')
            print('profile_id', profile_id)
            await state.finish()
            await IdeaStates.text.set()
            await state.update_data(profile_id=profile_id)


@dp.message_handler(text="📢 E'tiroz bildirish", state=GetProfileState.profile_id)
async def start_sending_idea(message: types.Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.answer(text="🚫 Sizda botdan foydalanish uchun ruxsat mavjud emas,\n"
                                  "📝 Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak 👇",
                             reply_markup=go_registration_default_keyboard)
    else:
        user = users[0]
        user_role = user['role']
        if user_role != 'parent':
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            await message.answer(text="✍️ E'tirozingizni yozing:",
                                 reply_markup=go_back_default_keyboard)
            data = await state.get_data()
            profile_id = data.get('profile_id')
            await state.finish()
            await Objection.text.set()
            await state.update_data(profile_id=profile_id)


@dp.message_handler(text="👏 Rag'bat bildirish", state=GetProfileState.profile_id)
async def start_sending_idea(message: types.Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.answer(text="🚫 Sizda botdan foydalanish uchun ruxsat mavjud emas,\n"
                                  "📝 Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak 👇",
                             reply_markup=go_registration_default_keyboard)
    else:
        user = users[0]
        user_role = user['role']
        if user_role != 'parent':
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            await message.answer(text="✍️ Rag'bat yozing:",
                                 reply_markup=go_back_default_keyboard)
            data = await state.get_data()
            profile_id = data.get('profile_id')
            await state.finish()
            await Incentive.text.set()
            await state.update_data(profile_id=profile_id)


@dp.message_handler(state=GetProfileState.profile_id)
async def get_child_function(message: types.Message, state: FSMContext):
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
    group = await db.select_group(group_id=group_id)
    teacher_id = group['teacher_id']
    teacher_profile = await db.select_teacher_profile(profile_id=teacher_id)
    teacher_user_id = teacher_profile['user_id']
    teacher_user = await db.select_user(user_id=teacher_user_id)
    experience = teacher_profile['experience']
    experience = experience if experience else "Hali kiritilmagan"
    age = (datetime.now().year - teacher_profile['birth_year']) if teacher_profile[
        'birth_year'] else "Hali kiritilmagan"
    text = (f"📚 O'qituvchi ma'lumotlari:\n"
            f"🧑‍💼 Ismi: {teacher_profile['first_name']}\n"
            f"👤 Familiyasi: {teacher_profile['last_name']}\n"
            f"📅 Yoshi: {age}\n"
            f"💼 Ish staji: {experience}\n"
            f"📞 Tel: {teacher_user['phone']}\n")

    await message.answer(text=text)
    await message.answer(
        text="📝O'qituvchiga quyidagi bo'limlardan birini tanlab, o'z xabaringizni qoldiring 👇",
        reply_markup=contact_default_keyboard
    )


# for ideas
@dp.callback_query_handler(state=IdeaStates.text, text="yes")
async def send_idea_finish(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print('data', data)
    idea = data.get("text")
    profile_id = data.get('profile_id')

    # user_telegram_id = call.from_user.id
    # users = await db.select_users(telegram_id=user_telegram_id)
    # user = users[0]
    # parent_profiles = await db.select_parent_profiles(user_id=user['id'])
    parent_profile = await db.select_parent_profile(profile_id=profile_id)
    student_full_name = f"{parent_profile['child_first_name']} {parent_profile['child_last_name']}"
    group_id = parent_profile['group_id']
    group = await db.select_group(group_id=group_id)
    teacher_id = group['teacher_id']
    teacher_profile = await db.select_teacher_profile(profile_id=teacher_id)
    teacher_full_name = f"{teacher_profile['first_name']} {teacher_profile['last_name']}"

    text = (f"💡💡 Yangi taklif:\n"
            f"👤 O'quvchi: {student_full_name}\n"
            f"👩‍🏫 O'qituvchi: {teacher_full_name}\n"
            f"🧠 Taklif: {idea}")
    await bot.send_message(chat_id=int(GROUP_CHAT_ID), text=text)
    await call.message.answer(text="✅ Jo'natildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text="no", state=IdeaStates.text)
async def cancel_sending_idea(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Jo'natish bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=IdeaStates.text)
async def get_idea_text(message: types.Message, state: FSMContext):
    idea = message.text
    await state.update_data(text=idea)
    text = (f"✨ Sizning taklifingiz: \n"
            f"Taklif: {idea}")
    await message.answer(text=text)
    await message.answer(text="Yuborishni xohlaysizmi❓", reply_markup=confirm_keyboard)


# for objection
@dp.callback_query_handler(state=Objection.text, text="yes")
async def send_objection_finish(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    objection = data.get("text")
    profile_id = data.get('profile_id')

    # user_telegram_id = call.from_user.id
    # users = await db.select_users(telegram_id=user_telegram_id)
    # user = users[0]
    # parent_profiles = await db.select_parent_profiles(user_id=user['id'])
    parent_profile = await db.select_parent_profile(profile_id=profile_id)
    student_full_name = f"{parent_profile['child_first_name']} {parent_profile['child_last_name']}"
    group_id = parent_profile['group_id']
    group = await db.select_group(group_id=group_id)
    teacher_id = group['teacher_id']
    teacher_profile = await db.select_teacher_profile(profile_id=teacher_id)
    teacher_full_name = f"{teacher_profile['first_name']} {teacher_profile['last_name']}"

    text = (f"🛑🛑 Yangi e'tiroz:\n"
            f"👤 O'quvchi: {student_full_name}\n"
            f"👩‍🏫 O'qituvchi: {teacher_full_name}\n"
            f"🗣️ E'tiroz matni: {objection}")
    await bot.send_message(chat_id=int(GROUP_CHAT_ID), text=text)
    await call.message.answer(text="✅ Jo'natildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text="no", state=Objection.text)
async def cancel_sending_objection(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Jo'natish bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=Objection.text)
async def get_objection_text(message: types.Message, state: FSMContext):
    objection = message.text
    await state.update_data(text=objection)
    text = (f"✨ Sizning e'tirozingiz: \n"
            f"E'tiroz: {objection}")
    await message.answer(text=text)
    await message.answer(text="Yuborishni xohlaysizmi❓", reply_markup=confirm_keyboard)


# for incentive
@dp.callback_query_handler(state=Incentive.text, text="yes")
async def send_incentive_finish(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    incentive = data.get("text")
    profile_id = data.get('profile_id')

    # user_telegram_id = call.from_user.id
    # users = await db.select_users(telegram_id=user_telegram_id)
    # user = users[0]
    # parent_profiles = await db.select_parent_profiles(user_id=user['id'])
    parent_profile = await db.select_parent_profile(profile_id=profile_id)
    student_full_name = f"{parent_profile['child_first_name']} {parent_profile['child_last_name']}"
    group_id = parent_profile['group_id']
    group = await db.select_group(group_id=group_id)
    teacher_id = group['teacher_id']
    teacher_profile = await db.select_teacher_profile(profile_id=teacher_id)
    teacher_full_name = f"{teacher_profile['first_name']} {teacher_profile['last_name']}"

    text = (f"🎉🎉 Yangi rag'bat:\n"
            f"👤 O'quvchi: {student_full_name}\n"
            f"👩‍🏫 O'qituvchi: {teacher_full_name}\n"
            f"🌟 Rag'bat matni: {incentive}")
    await bot.send_message(chat_id=int(GROUP_CHAT_ID), text=text)
    await call.message.answer(text="✅ Jo'natildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text="no", state=Incentive.text)
async def cancel_sending_incentive(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Jo'natish bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=Incentive.text)
async def get_incentive_text(message: types.Message, state: FSMContext):
    incentive = message.text
    await state.update_data(text=incentive)
    text = (f"✨ Sizning rag'batingiz: \n"
            f"Rag'bat: {incentive}")
    await message.answer(text=text)
    await message.answer(text="Yuborishni xohlaysizmi❓", reply_markup=confirm_keyboard)

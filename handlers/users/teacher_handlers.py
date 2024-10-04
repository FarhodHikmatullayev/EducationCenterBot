from aiogram import types
from aiogram.dispatcher import FSMContext
from django.db.models.fields import return_None

from keyboards.default.all_groups import my_groups_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.group_actions import group_actions_for_teachers
from keyboards.default.menu_keyboards import back_to_menu, go_back_default_keyboard
from loader import dp, db, bot
from states.groups import GetGroupState

@dp.message_handler(text="🔙 Orqaga", state=GetGroupState.group_id)
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
            markup = await my_groups_default_keyboard(teacher_id=teacher_id)
            await message.answer(text="Guruhlardan birini tanlang 👇", reply_markup=markup)
            await GetGroupState.group_id.set()


@dp.message_handler(state=GetGroupState.group_id)
async def get_group_id(message: types.Message, state: FSMContext):
    group_name = message.text
    groups = await db.select_groups(name=group_name)
    if not groups:
        await message.answer(text="⚠️ Bu guruh allaqachon o'chirib yuborilgan", reply_markup=go_back_default_keyboard)
        return
    group_id = groups[0]['id']
    await state.update_data(group_id=group_id)
    await message.answer(text="Amallardan birini tanlang 👇", reply_markup=group_actions_for_teachers)

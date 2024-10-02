from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import main_menu_default_keyboard
from loader import dp, db, bot


@dp.message_handler(text='🔙 Bosh Menyu', state='*')
@dp.message_handler(text="🤖 Botdan foydalanish 🤖", state='*')
async def go_to_menu_function(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if users:
        user = users[0]
        user_role = user['role']
        markup = await main_menu_default_keyboard(user_role=user_role)
        await message.answer(text="Bo'limlardan birini tanlang 👇", reply_markup=markup)

    else:
        await message.answer(text="🚫 Sizda botdan foydalanish uchun ruxsat mavjud emas,\n"
                                  "📝 Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak 👇",
                             reply_markup=go_registration_default_keyboard)

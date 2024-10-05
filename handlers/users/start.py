from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.menu_keyboards import use_bot_default_keyboard
from loader import dp, db, bot
from states.user_states import UserCreateStates


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    # await message.answer(text=f"{message.chat.id}")
    try:
        await state.finish()
    except:
        pass

    user_telegram_id = message.from_user.id
    username = message.from_user.username
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.reply(f"👋 Salom, Botimizga xush kelibsiz!")
        await message.answer("💬 Botdan foydalanish uchun ismingizni kiriting")
        await UserCreateStates.first_name.set()
        await state.update_data(telegram_id=user_telegram_id, username=username)

    else:
        user = users[0]
        user_full_name = user['full_name']
        await message.reply(f"👋 Salom, {user_full_name}!\n"
                            f"Botimizga xush kelibsiz")
        await message.answer(text="Botdan foydalanish tugmasini bosing 👇", reply_markup=use_bot_default_keyboard)


@dp.message_handler(text="📝 Ro'yxatdan o'tish", state='*')
async def register_function(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass

    user_telegram_id = message.from_user.id
    username = message.from_user.username
    await message.answer("💬 Iltimnos, ismingizni kiriting")

    await UserCreateStates.first_name.set()
    await state.update_data(telegram_id=user_telegram_id, username=username)


@dp.message_handler(state=UserCreateStates.first_name)
async def get_user_first_name(message: types.Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    await message.answer("💬 Familiyangizni kiriting")
    await UserCreateStates.last_name.set()


@dp.message_handler(state=UserCreateStates.last_name)
async def get_user_last_name(message: types.Message, state: FSMContext):
    last_name = message.text
    await state.update_data(last_name=last_name)
    await message.answer("📞 Iltimos, telefon raqamingizni kiriting\n"
                         "🔢 Misol: +998901234567")
    await UserCreateStates.phone_number.set()


@dp.message_handler(state=UserCreateStates.phone_number)
async def get_user_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone_number = data.get("phone_number")
    telegram_id = data.get("telegram_id")
    username = data.get("username")
    full_name = f"{first_name} {last_name}"
    user = await db.create_user(
        username=username,
        telegram_id=telegram_id,
        full_name=full_name,
        phone=phone_number
    )
    await state.finish()
    await message.answer(text="🎉 Siz botdan muvaffaqiyatli ro'yxatdan o'tdingiz! 🎊")
    await message.answer(text="Botdan foydalanish tugmasini bosing 👇", reply_markup=use_bot_default_keyboard)

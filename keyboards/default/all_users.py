from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


async def all_users_default_keyboard():
    users = await db.select_users(role='user')
    markup = ReplyKeyboardMarkup()
    markup.resize_keyboard = True
    markup.row_width = 2
    for user in users:
        text_button = f"{user['full_name']}"
        markup.insert(KeyboardButton(text_button))

    markup.insert(KeyboardButton(text="🔙 Orqaga"))

    return markup

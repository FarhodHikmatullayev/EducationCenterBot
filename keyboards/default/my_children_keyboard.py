from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


async def my_children_default_keyboard(user_id):
    parent_profiles = await db.select_parent_profiles(user_id=user_id)
    markup = ReplyKeyboardMarkup()
    markup.resize_keyboard = True
    markup.row_width = 2
    for child in parent_profiles:
        text_button = f"{child['child_first_name']} {child['child_last_name']}"
        markup.insert(KeyboardButton(text_button))

    markup.insert(KeyboardButton(text="🔙 Bosh Menyu"))

    return markup

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


async def all_students_in_group(group_id):
    parents = await db.select_parent_profiles(group_id=group_id)
    markup = ReplyKeyboardMarkup()
    markup.resize_keyboard = True
    markup.row_width = 2
    for parent in parents:
        text_button = f"{parent['child_first_name']} {parent['child_last_name']}"
        markup.insert(KeyboardButton(text_button))

    markup.insert(KeyboardButton(text="🔙 Orqaga"))

    return markup

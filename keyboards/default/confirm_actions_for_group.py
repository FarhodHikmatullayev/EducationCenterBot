from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

delete_group_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔙 Guruhlarga qaytish"),
            KeyboardButton(text="🗑️ O'chirish")
        ]
    ]
)

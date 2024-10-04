from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

delete_teacher_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔙 O'qituvchilarga qaytish"),
            KeyboardButton(text="🗑️ O'chirish")
        ]
    ]
)

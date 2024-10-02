from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

teacher_actions_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="➕ O'qituvchi qo'shish")
        ],
        [
            KeyboardButton(text="🗑️ O'qituvchini o'chirish")
        ],
        [
            KeyboardButton(text="✏️ O'qituvchini o'zgartirish")
        ],
        [
            KeyboardButton(text="🔙 Bosh Menyu")
        ]
    ]
)

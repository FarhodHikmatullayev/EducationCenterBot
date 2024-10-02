from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

group_actions_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="➕ Guruh qo'shish")
        ],
        [
            KeyboardButton(text="🗑️ Guruhni o'chirish")
        ],
        [
            KeyboardButton(text="✏️ Guruhni o'zgartirish")
        ],
        [
            KeyboardButton(text="🔙 Bosh Menyu")
        ]
    ]
)

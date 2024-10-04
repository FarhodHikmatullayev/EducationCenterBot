from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

group_actions_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="➕ Yangi guruh yaratish")
        ],
        [
            KeyboardButton(text="🗑️ Guruhni o'chirish")
        ],
        [
            KeyboardButton(text="✏️ Guruhni o'zgartirish")
        ],
        [
            KeyboardButton(text="➕ Guruhga o'quvchi qo'shish"),
            KeyboardButton(text="➖ Guruhdan o'quvchini o'chirish")
        ],
        [
            KeyboardButton(text="🔙 Bosh Menyu")
        ]
    ]
)

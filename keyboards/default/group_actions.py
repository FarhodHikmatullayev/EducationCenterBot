from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from states.groups import RemoveStudentFromGroupState

group_actions_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="➕ Yangi guruh yaratish")
        ],

        [
            KeyboardButton(text="🗑️ Guruhni o'chirish"),
            KeyboardButton(text="✏️ Guruhni o'zgartirish")
        ],
        [
            KeyboardButton(text="➕ Guruhga o'quvchi qo'shish"),
            KeyboardButton(text="➖ Guruhdan o'quvchini o'chirish")
        ],
        [
            KeyboardButton(text="📊 Guruh o'quvchilari reytingini ko'rish")
        ],
        [
            KeyboardButton(text="🔙 Bosh Menyu")
        ]
    ]
)

group_actions_for_teachers = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="✨ Guruhdagi o'quvchilarni baholash"),
        ],
        [
            KeyboardButton(text="📊 Guruh o'quvchilari reytingi"),
        ],
        [
            KeyboardButton(text="➕ O'quvchi qo'shish"),
            KeyboardButton(text="➖ O'quvchini o'chirish"),
        ],

        [
            KeyboardButton(text="🔙 Orqaga"),
        ],
    ]
)

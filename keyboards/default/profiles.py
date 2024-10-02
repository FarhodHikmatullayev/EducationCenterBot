from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

change_profile_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="✏️ Profilni o'zgartirish"),
        ],
        [
            KeyboardButton(text="🔙 Bosh Menyu"),
        ]
    ]
)

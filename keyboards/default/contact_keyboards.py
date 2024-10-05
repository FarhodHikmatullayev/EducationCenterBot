from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="📩 Taklif yuborish"),
        ],
        [
            KeyboardButton(text="📢 E'tiroz bildirish"),
        ],
        [
            KeyboardButton(text="👏 Rag'bat bildirish"),
        ],
        [
            KeyboardButton(text="🔙 Bosh Menyu"),
        ],
    ]
)

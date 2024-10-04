from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=" ✅ Ha", callback_data="yes"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data="no")
        ]
    ]
)
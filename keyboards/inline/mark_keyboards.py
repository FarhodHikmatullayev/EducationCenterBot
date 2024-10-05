from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

marks_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='1️⃣',
                callback_data="1"
            ),
            InlineKeyboardButton(
                text='2️⃣',
                callback_data="2"
            ),
            InlineKeyboardButton(
                text='3️⃣',
                callback_data="3"
            ),
            InlineKeyboardButton(
                text='4️⃣',
                callback_data="4"
            ),
            InlineKeyboardButton(
                text='5️⃣',
                callback_data="5"
            ),
        ]
    ]
)

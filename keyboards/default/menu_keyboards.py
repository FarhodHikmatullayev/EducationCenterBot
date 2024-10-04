from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back_to_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔙 Bosh Menyu"),
        ]
    ]
)

use_bot_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🤖 Botdan foydalanish 🤖")
        ]
    ]
)


async def main_menu_default_keyboard(user_role):
    if user_role == "admin":
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text="👩‍🏫 O'qituvchilar")  # O'qituvchilar tugmasi
                ],
                [
                    KeyboardButton(text="👥 Guruhlar")  # Guruhlar tugmasi
                ],
                [
                    KeyboardButton(text="👤 Mening Profilim")  # Mening profilim tugmasi
                ]
            ]
        )
    elif user_role == "parent":
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text="📊 Baholar reytingi")  # Baholar reytingi tugmasi
                ],
                [
                    KeyboardButton(text="📞 O'qituvchi bilan bog'lanish")  # O'qituvchi bilan bog'lanish tugmasi
                ],
                [
                    KeyboardButton(text="👤 Mening Profilim")  # Mening profilim tugmasi
                ]
            ]
        )
    elif user_role == "teacher":
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text="👥 Guruhlarim")  # Guruhlarim tugmasi
                ],
                [
                    KeyboardButton(text="👤 Mening Profilim")  # Mening profilim tugmasi
                ]
            ]
        )
    else:
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text="👤 Mening Profilim")  # Mening Profilim tugmasi
                ]
            ]
        )

    return markup

go_back_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔙 Orqaga")
        ]
    ]
)

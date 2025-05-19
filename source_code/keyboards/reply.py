from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отменить")]],
    resize_keyboard=True
)

remove_kb = ReplyKeyboardRemove()
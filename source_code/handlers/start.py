from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from source_code.keyboards.inline import start_keyboard

async def cmd_start(message: Message):
    await message.answer("Привет! Выберите действие:", reply_markup=start_keyboard())

def register(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))

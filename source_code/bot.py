import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import BOT_TOKEN, GKP_CHAT_ID
from source_code.form import Form

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отменить")]],
    resize_keyboard=True,
    one_time_keyboard=False
)


@dp.message(lambda message: message.text and message.text.lower() in {"❌ отменить", "/cancel"})
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "❌ Заявка отменена. Чтобы начать заново, введите /start",
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(Command("start"))
async def cmd_start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Составить заявку", callback_data="create_request")
    await message.answer("Привет! Выберите действие:", reply_markup=builder.as_markup())


@dp.callback_query(lambda c: c.data == "create_request")
async def process_create_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("ФИО БВП (укажите если была смена ФИО):", reply_markup=cancel_kb)
    await state.set_state(Form.full_name)


@dp.message(Form.full_name)
async def step_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Дата рождения:", reply_markup=cancel_kb)
    await state.set_state(Form.birth_date)


@dp.message(Form.birth_date)
async def step_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Дата пропажи:", reply_markup=cancel_kb)
    await state.set_state(Form.missing_date)


@dp.message(Form.missing_date)
async def step_missing_date(message: Message, state: FSMContext):
    await state.update_data(missing_date=message.text)
    await message.answer("Место пропажи:", reply_markup=cancel_kb)
    await state.set_state(Form.missing_place)


@dp.message(Form.missing_place)
async def step_missing_place(message: Message, state: FSMContext):
    await state.update_data(missing_place=message.text)
    await message.answer("Морг (обязательно указать, звоним или нет):", reply_markup=cancel_kb)
    await state.set_state(Form.morgue)


@dp.message(Form.morgue)
async def step_morgue(message: Message, state: FSMContext):
    await state.update_data(morgue=message.text)
    await message.answer("Дополнительно (нужны ли больницы в другом районе?):", reply_markup=cancel_kb)
    await state.set_state(Form.additional)


@dp.message(Form.additional)
async def step_additional(message: Message, state: FSMContext):
    await state.update_data(additional=message.text)
    await message.answer("Примечание (важные детали для ГКП):", reply_markup=cancel_kb)
    await state.set_state(Form.notes)


@dp.message(Form.notes)
async def step_notes(message: Message, state: FSMContext):
    await state.update_data(notes=message.text)

    # Получаем username пользователя
    username = message.from_user.username
    suggested_username = f"@{username}" if username else "не указано"
    await state.update_data(informer=suggested_username)

    # Предлагаем использовать username
    builder = InlineKeyboardBuilder()
    builder.button(text=f"✅ Да, использовать {suggested_username}", callback_data="use_username")
    builder.button(text="✏️ Ввести вручную", callback_data="edit_username")

    await message.answer(
        f"Используем ваш username как инфорга: <b>{suggested_username}</b>?",
        reply_markup=builder.as_markup()
    )
    await state.set_state(Form.informer)


@dp.callback_query(Form.informer, lambda c: c.data in {"use_username", "edit_username"})
async def handle_username_choice(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)

    if callback.data == "use_username":
        await callback.message.answer("Проверьте данные перед отправкой:")
        return await finalize_form(callback.message, state)
    else:
        await callback.message.answer("Введите инфорга (через @):")


@dp.message(Form.informer)
async def step_manual_informer(message: Message, state: FSMContext):
    await state.update_data(informer=message.text)
    await message.answer("Проверьте данные перед отправкой:")
    await finalize_form(message, state)


async def finalize_form(message: Message, state: FSMContext):
    data = await state.get_data()

    summary = (
        f"<b>📝 Проверьте данные заявки:</b>\n"
        f"<b>ФИО БВП:</b> {data['full_name']}\n"
        f"<b>Дата рождения:</b> {data['birth_date']}\n"
        f"<b>Дата пропажи:</b> {data['missing_date']}\n"
        f"<b>Место пропажи:</b> {data['missing_place']}\n"
        f"<b>Морг:</b> {data['morgue']}\n"
        f"<b>Дополнительно:</b> {data['additional']}\n"
        f"<b>Примечание:</b> {data['notes']}\n"
        f"<b>Инфорг:</b> {data['informer']}"
    )

    confirm_kb = InlineKeyboardBuilder()
    confirm_kb.button(text="✅ Подтвердить", callback_data="confirm_yes")
    confirm_kb.button(text="❌ Отменить", callback_data="confirm_no")

    await message.answer(summary, reply_markup=confirm_kb.as_markup())
    await state.set_state(Form.confirm)


@dp.callback_query(Form.confirm, lambda c: c.data in {"confirm_yes", "confirm_no"})
async def process_confirmation(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)

    if callback.data == "confirm_yes":
        data = await state.get_data()
        gkp_message = (
            f"<b>📝 Получена новая заявка</b>\n"
            f"<b>ФИО БВП:</b> {data['full_name']}\n"
            f"<b>Дата рождения:</b> {data['birth_date']}\n"
            f"<b>Дата пропажи:</b> {data['missing_date']}\n"
            f"<b>Место пропажи:</b> {data['missing_place']}\n"
            f"<b>Морг:</b> {data['morgue']}\n"
            f"<b>Дополнительно:</b> {data['additional']}\n"
            f"<b>Примечание:</b> {data['notes']}\n"
            f"<b>Инфорг:</b> {data['informer']}"
        )

        await bot.send_message(GKP_CHAT_ID, gkp_message)
        await callback.message.answer("✅ Заявка отправлена в ГКП!", reply_markup=ReplyKeyboardRemove())
    else:
        await callback.message.answer("❌ Заявка отменена", reply_markup=ReplyKeyboardRemove())

    new_request_kb = InlineKeyboardBuilder()
    new_request_kb.button(text="📝 Новая заявка", callback_data="create_request")
    await callback.message.answer("Хотите создать новую заявку?", reply_markup=new_request_kb.as_markup())
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

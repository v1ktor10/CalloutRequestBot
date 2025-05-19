from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from source_code.keyboards.inline import username_keyboard
from source_code.keyboards.reply import cancel_kb, remove_kb
from source_code.states.form import Form
from source_code.utils.finalize import finalize_form

async def process_create_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer("ФИО БВП (укажите если была смена ФИО):", reply_markup=cancel_kb)
    await state.set_state(Form.full_name)

async def step_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Дата рождения:", reply_markup=cancel_kb)
    await state.set_state(Form.birth_date)

async def step_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Дата пропажи:", reply_markup=cancel_kb)
    await state.set_state(Form.missing_date)

async def step_missing_date(message: Message, state: FSMContext):
    await state.update_data(missing_date=message.text)
    await message.answer("Место пропажи:", reply_markup=cancel_kb)
    await state.set_state(Form.missing_place)

async def step_missing_place(message: Message, state: FSMContext):
    await state.update_data(missing_place=message.text)
    await message.answer("Морг (обязательно указать, звоним или нет):", reply_markup=cancel_kb)
    await state.set_state(Form.morgue)

async def step_morgue(message: Message, state: FSMContext):
    await state.update_data(morgue=message.text)
    await message.answer("Дополнительно (нужны ли больницы в другом районе?):", reply_markup=cancel_kb)
    await state.set_state(Form.additional)

async def step_additional(message: Message, state: FSMContext):
    await state.update_data(additional=message.text)
    await message.answer("Примечание (важные детали для ГКП):", reply_markup=cancel_kb)
    await state.set_state(Form.notes)

async def step_notes(message: Message, state: FSMContext):
    await state.update_data(notes=message.text)
    username = message.from_user.username
    suggested_username = f"@{username}" if username else "не указано"
    await state.update_data(informer=suggested_username)
    await message.answer(
        f"Используем ваш username как инфорга: <b>{suggested_username}</b>?",
        reply_markup=username_keyboard(suggested_username)
    )
    await state.set_state(Form.informer)

async def step_manual_informer(message: Message, state: FSMContext):
    await state.update_data(informer=message.text)
    await message.answer("Проверьте данные перед отправкой:")
    await finalize_form(message, state)

async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Заявка отменена. Чтобы начать заново, введите /start", reply_markup=remove_kb)

def register(dp: Dispatcher):
    dp.callback_query.register(process_create_request, lambda c: c.data == "create_request")
    dp.message.register(cancel_handler, lambda msg: msg.text and msg.text.lower() in {"/cancel", "❌ отменить"})
    dp.message.register(step_full_name, Form.full_name)
    dp.message.register(step_birth_date, Form.birth_date)
    dp.message.register(step_missing_date, Form.missing_date)
    dp.message.register(step_missing_place, Form.missing_place)
    dp.message.register(step_morgue, Form.morgue)
    dp.message.register(step_additional, Form.additional)
    dp.message.register(step_notes, Form.notes)
    dp.message.register(step_manual_informer, Form.informer)
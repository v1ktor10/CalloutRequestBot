from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from source_code.config import GKP_CHAT_ID
from source_code.keyboards.inline import new_request_keyboard
from source_code.keyboards.reply import remove_kb
from source_code.states.form import Form
from source_code.utils.finalize import finalize_form

async def handle_username_choice(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    if callback.data == "use_username":
        await callback.message.answer("Проверьте данные перед отправкой:")
        await finalize_form(callback.message, state)
    else:
        await callback.message.answer("Введите инфорга (через @):")

async def process_confirmation(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    if callback.data == "confirm_yes":
        data = await state.get_data()
        message_text = (
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
        await callback.bot.send_message(GKP_CHAT_ID, message_text)
        await callback.message.answer("✅ Заявка отправлена в ГКП!", reply_markup=remove_kb)
    else:
        await callback.message.answer("❌ Заявка отменена", reply_markup=remove_kb)
    await callback.message.answer("Хотите создать новую заявку?", reply_markup=new_request_keyboard())
    await state.clear()

def register(dp: Dispatcher):
    dp.callback_query.register(handle_username_choice, Form.informer, lambda c: c.data in {"use_username", "edit_username"})
    dp.callback_query.register(process_confirmation, Form.confirm, lambda c: c.data in {"confirm_yes", "confirm_no"})

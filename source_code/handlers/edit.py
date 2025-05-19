from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from source_code.states.form import Form
from source_code.utils.finalize import finalize_form

async def handle_edit_field(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    field_map = {
        "edit_full_name": "full_name",
        "edit_birth_date": "birth_date",
        "edit_missing_date": "missing_date",
        "edit_missing_place": "missing_place",
        "edit_morgue": "morgue",
        "edit_additional": "additional",
        "edit_notes": "notes",
        "edit_informer": "informer",
    }

    field = field_map.get(callback.data)
    if field:
        await state.update_data(edit_field=field)
        prompts = {
            "full_name": "Введите ФИО БВП:",
            "birth_date": "Введите дату рождения (ДД.ММ.ГГГГ):",
            "missing_date": "Введите дату пропажи (ДД.ММ.ГГГГ):",
            "missing_place": "Введите место пропажи:",
            "morgue": "Введите название или номер морга:",
            "additional": "Введите дополнительную информацию (если есть):",
            "notes": "Введите примечания (если нужно):",
            "informer": "Введите инфорга (через @):",
        }
        await callback.message.answer(f"✏ {prompts[field]}")
        await state.set_state(Form.edit_field)

async def handle_edit_input(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data.get("edit_field")

    if not field:
        await message.answer("⚠ Произошла ошибка. Попробуйте снова.")
        return

    await state.update_data({field: message.text})
    await state.update_data(edit_field=None)
    await finalize_form(message, state)
    await state.set_state(Form.confirm)

def register(dp: Dispatcher):
    dp.callback_query.register(handle_edit_field, Form.confirm, lambda c: c.data.startswith("edit_"))
    dp.message.register(handle_edit_input, Form.edit_field)
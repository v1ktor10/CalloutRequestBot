from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from source_code.states.form import Form

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
        f"<b>Примечания:</b> {data['notes']}\n"
        f"<b>Инфорг:</b> {data['informer']}"
    )

    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Подтвердить", callback_data="confirm_yes")
    kb.button(text="❌ Отменить", callback_data="confirm_no")
    kb.button(text="✏ ФИО", callback_data="edit_full_name")
    kb.button(text="✏ Дата рождения", callback_data="edit_birth_date")
    kb.button(text="✏ Дата пропажи", callback_data="edit_missing_date")
    kb.button(text="✏ Место пропажи", callback_data="edit_missing_place")
    kb.button(text="✏ Морг", callback_data="edit_morgue")
    kb.button(text="✏ Дополнительно", callback_data="edit_additional")
    kb.button(text="✏ Примечания", callback_data="edit_notes")
    kb.button(text="✏ Инфорг", callback_data="edit_informer")
    kb.adjust(2, 2, 2, 2, 1)

    await message.answer(summary, reply_markup=kb.as_markup())
    await state.set_state(Form.confirm)

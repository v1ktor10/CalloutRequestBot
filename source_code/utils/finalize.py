from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from source_code.keyboards.inline import confirm_keyboard
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
        f"<b>Примечание:</b> {data['notes']}\n"
        f"<b>Инфорг:</b> {data['informer']}"
    )

    await message.answer(summary, reply_markup=confirm_keyboard())

    await state.set_state(Form.confirm)
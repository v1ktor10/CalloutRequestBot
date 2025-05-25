from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Составить заявку", callback_data="create_request")
    return kb.as_markup()

def username_keyboard(username: str):
    kb = InlineKeyboardBuilder()
    kb.button(text=f"✅ Да, использовать {username}", callback_data="use_username")
    kb.button(text="✏️ Ввести вручную", callback_data="edit_username")
    return kb.as_markup()

def confirm_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Подтвердить", callback_data="confirm_yes")
    kb.button(text="❌ Отменить", callback_data="confirm_no")
    return kb.as_markup()

def new_request_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Новая заявка", callback_data="create_request")
    return kb.as_markup()

def request_message_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="📞 Прозвон начал", callback_data="start_call")
    return kb.as_markup()
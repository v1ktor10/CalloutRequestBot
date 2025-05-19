from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    confirm = State()
    full_name = State()
    birth_date = State()
    missing_date = State()
    missing_place = State()
    morgue = State()
    additional = State()
    notes = State()
    informer = State()
    edit_field = State()
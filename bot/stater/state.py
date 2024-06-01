"""модуль для машинных состояние"""
from aiogram.fsm.state import State, StatesGroup

class USR(StatesGroup):
    """Название машинных состояний"""
    name=State()
    Groops=State()
    group_add=State()
    group_name_add=State()
    edu_add=State()
    group_user_add=State()

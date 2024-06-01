"""Модуль кнопок администратора"""
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.model import EDU

def edu():
    """Функиция для вывода список учебных заведений в виде кнопок"""
    keyboard= InlineKeyboardBuilder()
    i=False
    for edu_name in EDU.select(EDU.edu_name).dicts():

        keyboard.add(InlineKeyboardButton(text=f"{edu_name["edu_name"]}",
            callback_data=f'edu_{edu_name["edu_name"]}'
            ))
        i=True

    if i:
        return keyboard.adjust(2).as_markup()
    return i

"""Модуль для создания кнопок"""
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.model import Group

Keyboard_register = InlineKeyboardMarkup(inline_keyboard=[
    [
    InlineKeyboardButton(text="Преподаватель",callback_data='Преподаватель'),
    InlineKeyboardButton(text="Студент",callback_data='Студент')
    ]])

def group():
    """Функция для вывода кнопок с группами"""
    keyboard= InlineKeyboardBuilder()
    i=False
    for group_name in Group.select(Group.group_name).dicts():

        keyboard.add(InlineKeyboardButton(text=f"{group_name["group_name"]}",
            callback_data=f'group_{group_name["group_name"]}'
            ))
        i=True

    if i:
        return keyboard.adjust(2).as_markup()
    return i

def teach_or_not(name):
    """создание кнопок для подтверждения"""
    keyboard= InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Подтвердить",callback_data=f'name1_{name}'),
        InlineKeyboardButton(text='Отказать',callback_data=f'name_{name}')
    ]])
    return keyboard

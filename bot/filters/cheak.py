"""Библеотеки для проверки пользователя"""
from aiogram.filters import BaseFilter
from aiogram.types import Message
from database.model import User

class Cheakteacher(BaseFilter):
    """Проверяет является ли пользователь преподователем"""
    async def __call__ (self,message:Message):
        user = User.get_or_none(User.chat_id == message.from_user.id)
        if user and user.Teacher:
            return True
        return False

class Cheakstudent(BaseFilter):
    """Проверяет является ли пользователь студентом"""
    async def __call__ (self,message:Message):
        user = User.get_or_none(User.chat_id == message.from_user.id)
        if user and user.Student:
            return True
        return False

class Cheakadmin(BaseFilter):
    """Проверяет является ли пользователь студентом"""
    async def __call__ (self,message:Message):
        user = User.get_or_none(User.chat_id == message.from_user.id)
        if user.Admin:
            return True
        return False

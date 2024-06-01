"""Модуль обработки команд администратора"""
from aiogram.types import Message, BotCommand,CallbackQuery
from aiogram.fsm.context import FSMContext
from database.model import Group,EDU,User
import bot.stater.state as stat
import bot.keys_board.admin as admin

async def menu_admin(message:Message,state:FSMContext) -> None:
    """""
    Функция для вывода меню
    """
    await state.clear()
    # pylint: disable=C0415:
    from main import bot
    commands = [
        BotCommand(command="/group", description="Создать Группу"),
        BotCommand(command="/menu", description="Меню"),
        BotCommand(command="/edu_add", description="Добавить учебное заведение")
    ]
    await bot.set_my_commands(commands)
    await message.answer("Команды находятся слева в углу")

async def group_add(message:Message,state:FSMContext):
    """Создание группы"""
    edu=admin.edu()
    if edu:
        await message.answer("Выберите учебное заведение",reply_markup=edu)
        await state.set_state(stat.USR.group_add)
        await message.delete()
    else:
        await message.answer("Нет учебных заведений")

async def group_edu_add(callbak:CallbackQuery,state:FSMContext):
    """Добавление в учебное заведение группы"""
    await callbak.message.delete()
    await state.update_data({'edu': callbak.data.split('_')[1]})
    await callbak.message.answer("Введите название группы")
    await state.set_state(stat.USR.group_name_add)

async def group_name(message:Message,state:FSMContext):
    """Создание названия группы"""
    Group.get_or_create(
        user_creator=User.get(User.chat_id == message.from_user.id).Admin,
        group_name=message.text,
        edu=EDU.get(EDU.edu_name == (await state.get_data())['edu'])
        )
    await message.answer("Группа добавленна в список")
    await state.clear()

async def edu_add(message:Message,state:FSMContext):
    """Добавление учебного заведения"""
    await message.answer("Введите название учебного заведения")
    await state.set_state(stat.USR.edu_add)

async def edu_name(message:Message,state:FSMContext):
    """Добавление названия учебного заведения"""
    EDU.get_or_create(
        user_creator=User.get(User.chat_id == message.from_user.id).Admin,
        edu_name=message.text
        )
    await message.answer("Учебное заведение добавленна в список")
    await state.clear()

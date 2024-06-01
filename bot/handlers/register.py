"""Модуль обработки регистраций"""
import re
from ast import literal_eval
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext
from database.model import User,Student,Teacher,Group,TeacherOrNo,Admin
import bot.stater.state as stat
import bot.keys_board.register as reg

async def command_start_handler(message: Message,state :FSMContext) -> None:
    """"
    Обработчик команды /start
    Ввод ФИО
    """
    user=bool(User.get_or_none(User.chat_id == message.from_user.id) is None)
    if user:
        await message.answer("Введите ФИО")
        await state.set_state(stat.USR.name)

    else:
        user=User.get(User.chat_id == message.from_user.id)
        await message.answer(
            f"Вы уже зарегистрированы\n {user.user_name}, Выберите роль",
            reply_markup=reg.Keyboard_register
            )

async def name_user(message: Message,state :FSMContext) -> None:
    """
    Обработчик ввода ФИО
    """
    text= message.text
    if isinstance(text,str):
        user_name=text.split()  # Разделение строки на список слов
        result = "".join(user_name)

        if len(user_name) !=3  and len(user_name) !=2:
            await message.answer("Введите ФИО!1")
            await state.set_state(stat.USR.name)
        elif re.search(r'[^а-яА-Я-]',result):
            await message.answer("Должена быть только Кириллица!")
            await message.answer("Введите ФИО2")
            await state.set_state(stat.USR.name)
        elif (len(result.split('-'))!=3 and len(result.split('-'))!=4
            and len(result.split('-'))!=2 and len(result.split('-'))!=1):
            await message.answer("Введите ФИО!3")
            await state.set_state(stat.USR.name)
        elif re.search(r'--+',result):
            await message.answer("Введите ФИО!4")
            await state.set_state(stat.USR.name)
        else:
            initials = [name[0].upper() + '.' for name in user_name[1:]]
            user=user_name[0][0].upper()+user_name[0][1::] + ' ' + ' '.join(initials)

        # Приветствие с выбором типа профиля
            User.get_or_create(
                chat_id = message.from_user.id,#  Chat - ID пользователя
                user_name= user,
                )
            await message.answer(
            f"Привет, {user}!\nВыберите роль",reply_markup=reg.Keyboard_register)
    else:
        await message.answer("Введите ФИО!5")
        await state.set_state(stat.USR.name)

# Регистрация профиля студента

async def student_registr(callbak :CallbackQuery,state: FSMContext):
    """Обработчик ввода или выбора группы"""
    await callbak.message.delete()
    await callbak.answer("")
    # Обновление данных. Изменяет ранг на ранг Студента
    groups=reg.group()
    if groups:
        await callbak.message.answer("Выберите свою группу",reply_markup=groups)
        await state.set_state(stat.USR.Groops)
    else:
        await callbak.message.answer("На данный момент групп нет")

async def sudent_groops(callbak:CallbackQuery,state: FSMContext,):
    """Обработчик завершения регестраций"""
    await callbak.message.delete()
    user=User.get(User.chat_id == callbak.message.chat.id)
    group=Group.get(Group.group_name == callbak.data.split('_')[1])
    Student.get_or_create(user=user,group=group)
    await state.clear()
    await callbak.message.answer("Вы зарегестрированы.")
# Ожидание подтверждения профиля от преподавателя.
# Рассылка другим преподавателям запроса с подтверждением

async def teacher_confirmed(callbak:CallbackQuery):
    """Обработчик расслыки на подтверждение"""
    await callbak.message.answer("Ожидание подтверждения")
    message_id={}
    user=User.get(User.chat_id == callbak.message.chat.id)
    teacher=Teacher.select().dicts()
    if teacher:
        for i in Teacher.select().dicts():
            i=User.get(i['user']).chat_id
        # Получаем данные из таблицы Teacher и отправляем им запрос на подтверждение
            message_info = await callbak.bot.send_message(
                i, user.user_name + ', Вы являетесь преподавателем?',
                reply_markup=reg.teach_or_not(callbak.message.chat.id)
            )
            message_id[i]=message_info.message_id
        TeacherOrNo.get_or_create(
                            user=user,
                            message_id=message_id
                        )
    for i in Admin.select().dicts():
        i=User.get(i['user']).chat_id
    # Получаем данные из таблицы Teacher и отправляем им запрос на подтверждение
        message_info = await callbak.bot.send_message(
            i, user.user_name + ', Вы являетесь преподавателем?',
            reply_markup=reg.teach_or_not(callbak.message.chat.id)
        )
        message_id[i]=message_info.message_id
    TeacherOrNo.get_or_create(
                        user=user,
                        message_id=message_id
                    )
    await callbak.message.delete()
# Подтверждение подлиности профиля новоприбывшего преподавателя

async def teacher_registr(callbak: CallbackQuery):
    """Обработчик принятия"""
    user = callbak.data.split('_')[1]
    user=User.get(User.chat_id == user)
    teacher=TeacherOrNo.get(user==user)
    await callbak.bot.send_message(
        user.chat_id,user.user_name+" Вы добавлены в список преподователей"
        )
    for i,y in literal_eval(teacher.message_id).items():
        await callbak.bot.delete_message(int(i), int(y))
    Teacher.get_or_create(user=user)
    teacher.delete_instance()

# Откидывается левый аккаунт

async def not_teach(callbak: CallbackQuery):
    """Обработчик отклонения"""
    user1 = callbak.data.split('_')[1]
    user=User.get(User.chat_id == user1)
    teacher=TeacherOrNo.get(user == user)
    teacher.delete_instance()
    await callbak.bot.send_message(user.chat_id,user.user_name+", Вы не преподаватель")
    for i,y in literal_eval(teacher.message_id).items():
        await callbak.bot.delete_message(int(i), int(y))
    await callbak.message.answer(
            f"Привет, {user.user_name}!\nВыберите роль",reply_markup=reg.Keyboard_register)
    # Сносит левого черта из БД преподавателй

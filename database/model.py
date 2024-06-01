"""Модуль для создание БД"""
from peewee import SqliteDatabase, Model,CharField,ForeignKeyField

db = SqliteDatabase('sqlite.db')

class Table(Model):
    """БД"""
    class Meta:
        """БД"""
        database = db

class User(Table):
    """Пользователь"""
    chat_id=CharField()
    user_name = CharField()

class Admin(Table):
    """Администратор"""
    user = ForeignKeyField(User, backref='Admin')

class EDU(Table):
    """Образовательное заведение"""
    user_creator=ForeignKeyField(Admin, backref='EDU')
    edu_name=CharField(unique=True)

class Teacher(Table):
    """Преподаватель"""
    user = ForeignKeyField(User, backref='Teacher')

class Group(Table):
    """Группа"""
    user_creator=ForeignKeyField(Admin, backref='Group')
    group_name=CharField(unique=True)
    edu=ForeignKeyField(EDU, backref='Group')

class Student(Table):
    """Студент"""
    user = ForeignKeyField(User, backref='Student')
    group = ForeignKeyField(Group,backref='Student')

class TeacherOrNo(Table):
    """Преподаватель или нет"""
    user = ForeignKeyField(User, backref='TeacherOrNo')
    message_id = CharField()

def admin_add():
    """Добавление администратора"""
    User.get_or_create(
        chat_id='1975886539',
        user_name='Проходимец'
    )
    Admin.get_or_create(user=User.get(User.chat_id == '1975886539'))

def start_db():
    """Создание|запуск БД"""
    db.connect()
    db.create_tables([User,Student,Admin,Teacher,Group,EDU,TeacherOrNo], safe=True)
    admin_add()
    db.close()
# for admin in Admin.select().dicts():
#     print(User.get(admin['user']).chat_id)

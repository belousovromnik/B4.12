"""
структура таблиц для наглядности
CREATE TABLE athelete(
    "id" integer primary key autoincrement,
    "age" integer,
    "birthdate" text,
    "gender" text,
    "height" real,
    "name" text,
    "weight" integer,
    "gold_medals" integer,
    "silver_medals" integer,
    "bronze_medals" integer,
    "total_medals" integer,
    "sport" text,
    "country" text);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE user(
    "id" integer primary key autoincrement,
    "first_name" text,
    "last_name" text,
    "gender" text,
    "email" text,
    "birthdate" text,
    "height" real);
"""

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = input("Пол: ")
    email = input("Адрес электронной почты: ")
    birthdat = input("День рождения, в формате ГГГГ-ММ-ДД: ")
    height = float(input("Рост в см, напр. 175: "))
    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdat,
        height=height
    )
    # возвращаем созданного пользователя
    return user


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()

    user = request_data()
    # добавляем нового пользователя в сессию
    session.add(user)
    # сохраняем все изменения, накопленные в сессии
    session.commit()
    print("Спасибо, данные сохранены!")


if __name__ == "__main__":
    main()

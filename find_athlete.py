import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from datetime import datetime

from users import User

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class Athelete(Base):
    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


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


def find_athelete(my_height, my_birthdate, session):
    man = session.query(Athelete).all()
    height_name, height_height = '', 0
    birthdate_name, birthdate_birthdate = '', ''
    height_min = abs(man[0].height * 100 - my_height)
    birthdate_min = abs(datetime.strptime(man[0].birthdate, '%Y-%m-%d') - my_birthdate).days
    for item in man:
        if item.height:
            item_min_height = abs(item.height * 100 - my_height)
            if height_min > item_min_height:
                height_min = item_min_height
                height_name = item.name
                height_height = item.height

        if item.birthdate:
            item_min_birthdate = abs(datetime.strptime(item.birthdate, '%Y-%m-%d') - my_birthdate).days
            if birthdate_min > item_min_birthdate:
                birthdate_min = item_min_birthdate
                birthdate_name = item.name
                birthdate_birthdate = item.birthdate

    print('Ближайщий по росту {}, рост {}'.format(height_name, height_height))
    print('Ближайщий по дате рождения {}, рост {}'.format(birthdate_name, birthdate_birthdate))


def find_user(name, session):
    """
    Производит поиск пользователя в таблице user по заданному имени name
    """
    # нахдим все записи в таблице User, у которых поле User.first_name совпадает с парарметром name
    query = session.query(User).filter(User.first_name == name).first()
    if not query:
        query = session.query(User).filter(User.last_name == name).first()

    return query


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()

    name = input("Введи имя пользователя для поиска: ")
    my_user = find_user(name, session)
    if my_user:
        my_height = my_user.height
        my_birthdate = datetime.strptime(my_user.birthdate, '%Y-%m-%d')
        find_athelete(my_height, my_birthdate, session)
    else:
        print("Пользователей с таким именем нет.")


if __name__ == "__main__":
    main()

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Создаем соединение с базой данных
engine = create_engine('mysql+pymysql://root:1q2w3e4r@localhost/py_project')

# Создаем сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Создаем базовый класс для моделей
Base = declarative_base()

# Определяем модель для таблицы users
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    login = Column(String(45), unique=True)
    password = Column(String(45))
    gender = Column(String(45))

class SavedSong(Base):
    __tablename__ = 'saved_songs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    song_name = Column(String(100))
    artist = Column(String(100))
    lyrics = Column(String)
    chords = Column(String)
    
    user = relationship("User", back_populates="saved_songs")

User.saved_songs = relationship("SavedSong", order_by=SavedSong.id, back_populates="user")

'''
# Получаем всех пользователей из таблицы users
users = session.query(User).all()
# Выводим имена пользователей
for user in users:
    print(user.login)

# Закрываем сессию
session.close()
'''
# Приложение для распознавания и поиска текстов и аккордов песен SongFinder

## Описание программы
Десктопное приложение для платформы Windows 10 предназначено для 
записи звуковых файлов, их последующего распознавания и определения 
названия песни. Приложение также предоставляет пользователю 
возможность получить текст песни и аккорды (для определенных
композиций). Этот проект предоставит пользователям удобный способ 
идентифицировать музыкальные произведения. Основная задача проекта -
создание удобного инструмента для пользователей, желающих определить 
название и содержание песен.
### База данных:
#### Создание базы данных
1. Откройте MySQL Workbench.
2. Нажмите на плюс рядом с MySQL connections
3. Введите имя базы данных, например, py_project и создайте для нее пароль ("Store in Vault..." - кнопка)
4. Нажмите "OK" для создания connection
5. После открытия сервера выберите в верхнем меню кнопку создания cхемы ("Create a new schema in the connected server")
6. В появившемся окне ввести py_project, нажать кнопку "Apply" и далее также "Apply" и "Finish" 

#### Создание таблиц
1. Введите запрос в Query для создания таблицы users:
```
USE py_project;
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    login VARCHAR(45) UNIQUE NOT NULL,
    password VARCHAR(45) NOT NULL,
    gender VARCHAR(45)
);
```
2. Введите запрос в Query для создания таблицы saved_songs:
```
USE py_project;
CREATE TABLE saved_songs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    song_name VARCHAR(100),
    artist VARCHAR(100),
    lyrics TEXT,
    chords TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```
#### Подключение базы данных
1. Создайте файл .env
2. Введите данные:
```
PASSWORD="your_password"
NAME="your_schema_name"
```

### Как запустить проект
1. Зайдите в Anaconda Powershell Prompt, перейдите в папку с проектом, создайте и активируйте виртуальное окружение
```
cd полный_путь_до_папки_с_проектом
conda activate
conda create --name venv
conda activate venv
```
2. Установите необходимые зависимости, выполнив команды
```
conda install ffmpeg
pip install -r requirements.txt
```
3. Запустите приложение:
```
python registration.py
```

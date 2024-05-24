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
### Импортируйте данные из файла SQL-дампа в новую базу данных:
Откройте консоль MySQL на другом компьютере.
Введите следующую команду, заменив DUMPFILE.sql на фактическое имя вашего файла SQL-дампа:
bash
```
mysql -uroot -p1q2w3e4r py_project < DUMPFILE.sql
```

### Как запустить проект
1. Создайте и активируйте виртуальное окружение
```
python -m venv venv
venv\Scripts\activate
```
2. Установите необходимые зависимости, выполнив команду:
```
pip install -r requirements.txt
```
3. Запустите приложение:
```python
python registration.py
```

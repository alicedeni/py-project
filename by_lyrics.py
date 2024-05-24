import requests
from bs4 import BeautifulSoup
import re

def find_song_info(lyrics):
    """
    Функция для поиска информации о песне по тексту песни.
    
    Args:
        lyrics (str): Текст песни.
    
    Returns:
        tuple: Кортеж, содержащий название песни, исполнителя, текст песни и аккорды.
    """
    # API endpoint для поиска информации о песне
    api_url = "https://api.genius.com/search"

    # Подготовка заголовков запроса
    headers = {
        "Authorization": "Bearer UwCaaUZgLrfr46kgUIZr40B3iH_RjZgjXEqjZhAbyJQoh7J99CPs4hQLG3wwhxIo"
    }

    # Подготовка данных запроса
    data = {
        "q": lyrics
    }

    # Отправка запроса
    response = requests.get(api_url, headers=headers, params=data)

    # Проверка успешности ответа
    if response.status_code == 200:
        # Разбор JSON-ответа
        response_json = response.json()

        # Извлечение названия песни и исполнителя
        song_info = response_json["response"]["hits"][0]["result"]
        song_title = song_info["title"]
        artist = song_info["artist_names"]

        # Получение URL песни
        song_url = song_info["url"]

        # Получение текста песни
        lyrics = get_song_lyrics(song_url)

        # Получение аккордов песни
        chords = get_song_chords(song_title, artist)

        # Возврат названия песни, исполнителя, текста и аккордов
        return song_title, artist, lyrics, chords

    # Если ответ был неуспешным, возвращаем None
    return None, None, None, None

def get_song_lyrics(song_url):
    """
    Функция для получения текста песни из URL страницы Genius.
    
    Args:
        song_url (str): URL страницы песни на Genius.
    
    Returns:
        str: Текст песни.
    """
    # Получение текста песни из URL страницы Genius
    page = requests.get(song_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    lyrics_container = soup.find("div", {"data-lyrics-container": "true"})
    if lyrics_container:
        lyrics = lyrics_container.get_text(separator="\n")
    else:
        lyrics = "Не удалось найти текст песни на странице."
    return lyrics

def get_song_chords(song_title, artist):
    """
    Функция для получения аккордов песни с сайта Chorder.ru.
    
    Args:
        song_title (str): Название песни.
        artist (str): Исполнитель песни.
    
    Returns:
        str: Аккорды песни.
    """
    url = f"https://chorder.ru/search?q={artist}+{song_title}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # Найти первый результат поиска
    song_links = soup.find_all("a")
    song_link = ''
    for i in song_links:
        if '/songs/' in str(i):
            song_link = i
            break
    if not song_link:
        return "Песня не найдена"
    
    # Перейти на страницу песни
    song_url = "https://chorder.ru" + song_link["href"]
    song_response = requests.get(song_url)
    song_soup = BeautifulSoup(song_response.text, "html.parser")
    song_text = remove_html_tags(str(song_soup.find("pre")))
    if song_text:
        return song_text
    else:
        return "Не удалось найти аккорды для указанной песни."


def remove_html_tags(text):
    """
    Функция для удаления HTML-тегов из текста.
    
    Args:
        text (str): Текст с HTML-тегами.
    
    Returns:
        str: Текст без HTML-тегов.
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
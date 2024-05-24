import os  # Модуль для работы с операционной системой
import re  # Модуль для работы с регулярными выражениями
import speech_recognition as sr  # Модуль для распознавания речи
import requests  # Модуль для отправки HTTP-запросов
from pydub import AudioSegment  # Модуль для работы с аудиофайлами
from bs4 import BeautifulSoup  # Модуль для парсинга HTML
from ShazamAPI import Shazam  # Модуль для работы с API Shazam

def search_song_from_file(file_path):
    """
    Функция для поиска информации о песне из аудиофайла.
    
    Args:
        file_path (str): Путь к аудиофайлу.
    
    Returns:
        tuple: Кортеж, содержащий название песни, текст песни, аккорды и исполнителя.
    """
    # Загрузка аудиофайла
    song = AudioSegment.from_file(file_path)
    
    # Сохранение аудио в формате WAV для распознавания речи
    wav_file = os.path.splitext(os.path.basename(file_path))[0] + ".wav"
    song.export(wav_file, format="wav")
    
    # Поиск названия, текста и аккордов песни
    song_name, song_lyrics, song_chords, song_artist = find_song_info(wav_file)
    
    # Удаление временного WAV-файла
    os.remove(wav_file)
    
    return song_name, song_lyrics, song_chords, song_artist

def find_song_info(wav_file):
    """
    Функция для поиска информации о песне из WAV-файла.
    
    Args:
        wav_file (str): Путь к WAV-файлу.
    
    Returns:
        tuple: Кортеж, содержащий название песни, текст песни, аккорды и исполнителя.
    """
    song_title = "Не удалось распознать текст песни."
    song_artist = "Не удалось распознать текст песни."
    song_lyrics = "Не удалось распознать текст песни."
    song_chords = "Не удалось получить аккорды к песне."
    # Распознавание речи в аудиофайле
    r = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio = r.record(source)
    
    try:
        # Распознавание текста песни
        '''
        song_text = r.recognize_google(audio, language="ru-RU")
        print("Распознанный текст песни:", song_text)
        '''
        
        # Поиск названия песни через API Shazam
        shazam = Shazam(open(wav_file, 'rb').read())
        recognize_generator = shazam.recognizeSong()
        response = next(recognize_generator)[1]
        
        if 'track' in response:
            song_title = response['track']['title']
            song_artist = response['track']['subtitle']
            print("Название песни:", song_title)
            print("Исполнитель:", song_artist)
        else:
            song_title = "Не удалось определить название песни."
            song_artist = "Не удалось определить исполнителя."
        if song_title != "Не удалось определить название песни.":
            # Поиск текста песни через API Genius
            genius_api_url = f"https://api.genius.com/search?q={song_title}"
            print(genius_api_url)
            genius_response = requests.get(genius_api_url, headers={"Authorization": "Bearer UwCaaUZgLrfr46kgUIZr40B3iH_RjZgjXEqjZhAbyJQoh7J99CPs4hQLG3wwhxIo"})
            genius_data = genius_response.json()
            
            if genius_data["response"]["hits"]:
                song_url = ''
                for i in genius_data["response"]["hits"]:
                    if song_artist in i["result"]["artist_names"]:
                        song_url = i["result"]["url"]
                if song_url:
                    song_lyrics = get_song_lyrics(song_url)
            else:
                song_lyrics = "Не удалось найти текст песни."
            
        else:
            song_lyrics = "Не удалось распознать текст песни."
            song_chords = "Не удалось получить аккорды к песне."
    
    except sr.UnknownValueError:
        song_title = "Не удалось распознать текст песни."
        song_artist = "Не удалось распознать текст песни."
        song_lyrics = "Не удалось распознать текст песни."
        song_chords = "Не удалось получить аккорды к песне."
    song_chords = get_song_chords(song_title, song_artist)
    
    return song_title, song_lyrics, song_chords, song_artist

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
    print(url)
    # Определение User-Agent
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    
    # Определение параметров запроса
    params = {
        'allow_redirects': True,
        'headers': {
            'User-Agent': user_agent
        }
    }
    
    response = requests.get(url, **params)
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
    if song_text and song_text != "None":
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
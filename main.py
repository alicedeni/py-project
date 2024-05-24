from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from settings import SettingsWindow
from search import SearchWindow
from by_audio import search_song_from_file  # Импорт функции из search_song.py
import pyaudio
import wave
import speech_recognition as sr
import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QScrollArea
from mydb import session, User, SavedSong

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, current_user):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('main_window.ui', self)
        self.ui.settings_btn.clicked.connect(self.show_settings_window)
        self.ui.search_btn.clicked.connect(self.show_search_window)
        self.ui.lad_btn.clicked.connect(self.load_song)
        self.ui.record.clicked.connect(self.listen)
        self.ui.cancel_btn.clicked.connect(self.cancel)
        self.ui.view_btn.clicked.connect(self.show_song_details)
        self.ui.save_btn.clicked.connect(self.save_song)
        self.ui.saved_btn.clicked.connect(self.show_saved_songs)
        self.current_user = current_user
        self.recording = False

        self.ui.hello.setText(f"Привет, {self.current_user.login}!")

        icon = QIcon()
        icon.addFile("icons/mic.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.ui.record.setIcon(icon)
        self.setWindowIcon(QIcon('icons/window.png'))
        self.song_name, self.song_lyrics, self.song_chords, self.song_artist = '', '', '', ''

    def show_settings_window(self):
        """
        Метод для отображения окна настроек.
        """
        self.settings_window = SettingsWindow(self.current_user)
        self.settings_window.show()
        self.close()

    def show_search_window(self):
        """
        Метод для отображения окна поиска.
        """
        self.search_window = SearchWindow(self.current_user)
        self.search_window.show()
        self.close()
    
    def show_saved_songs(self):
        """
        Метод для отображения сохраненных песен пользователя.
        """
        saved_songs = session.query(SavedSong).filter_by(user_id=self.current_user.id).all()

        if saved_songs:
            songs_info = ""
            for song in saved_songs:
                songs_info += f"{song.song_name} - {song.artist}\n"
                if song.chords:
                    songs_info += f"Аккорды:\n{song.chords}\n\n"
                elif song.lyrics:
                    songs_info += f"Текст:\n{song.lyrics}\n\n"
                else:
                    songs_info += "Текст или аккорды недоступны.\n\n"
            self.ui.song_label.setText(songs_info)
        else:
            self.ui.song_label.setText("У вас пока нет сохраненных песен.")

    def save_song(self):
        """
        Метод для сохранения песни в базе данных.
        """
        saved_song = SavedSong(
            user_id=self.current_user.id,
            song_name=self.song_name,
            artist=self.song_artist,
            lyrics=self.song_lyrics,
            chords=self.song_chords
        )

        session.add(saved_song)

        session.commit()

    def show_song_details(self):
        """
        Метод для отображения деталей песни.
        """
        if self.song_name and self.song_chords:
            self.ui.song_label.setText(f"{self.song_name} - {self.song_artist}\n\nАккорды:\n{self.song_chords}")
        elif self.song_name and self.song_lyrics:
            self.ui.song_label.setText(f"{self.song_name} - {self.song_artist}\n\nТекст:\n{self.song_lyrics}")
        else:
            self.ui.song_label.setText("Не удалось определить текст или аккорды песни.")

    def load_song(self):
        """
        Метод для загрузки песни из аудиофайла.
        """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите аудиофайл", "", "Audio Files (*.mp3)")
        if file_path:
            self.song_name, self.song_lyrics, self.song_chords, self.song_artist = search_song_from_file(file_path)
            if self.song_name:
                self.ui.song_label.setText(f"{self.song_name} - {self.song_artist}")
            else:
                self.ui.song_label.setText("Не удалось определить название и исполнителя песни.")

    def listen(self):
        """
        Метод для записи аудио и поиска песни по аудио.
        """
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 15
        WAVE_OUTPUT_FILENAME = "output.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        self.recording = True

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            if not self.recording: 
                break
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        self.song_name, self.song_lyrics, self.song_chords, self.song_artist = search_song_from_file("output.wav")
        if self.song_name:
            self.ui.song_label.setText(f"{self.song_name} - {self.song_artist}")
        else:
            self.ui.song_label.setText("Не удалось определить название и исполнителя песни.")
    
    def cancel(self):
        """
        Метод для отмены записи аудио.
        """
        self.recording = False
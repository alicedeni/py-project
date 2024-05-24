from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from by_lyrics import find_song_info
from mydb import session, User, SavedSong

class SearchWindow(QtWidgets.QMainWindow):
    def __init__(self, current_user):
        super(SearchWindow, self).__init__()
        self.ui = uic.loadUi('search_window.ui', self)
        
        # Подключение сигналов кнопок к соответствующим методам
        self.ui.return_btn.clicked.connect(self.show_main_window)
        self.ui.settings_btn.clicked.connect(self.show_settings_window)
        self.ui.view_btn.clicked.connect(self.show_song_details)
        self.ui.save_btn.clicked.connect(self.save_song)
        self.ui.saved_btn.clicked.connect(self.show_saved_songs)
        
        # Установка иконки для окна приложения
        self.setWindowIcon(QIcon('icons/window.png'))
        
        self.current_user = current_user

        # Отображение приветственного сообщения для пользователя
        self.ui.hello.setText(f"Привет, {self.current_user.login}!")

        # Установка иконки для кнопки поиска
        icon = QIcon()
        icon.addFile("icons/search.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.ui.search_btn.setIcon(icon)

        # Подключение кнопки поиска к методу поиска текста
        self.ui.search_btn.clicked.connect(self.search_text) 
        
        # Инициализация переменных для хранения информации о песне
        self.song_title, self.artist, self.lyric, self.chords = '', '', '', ''

    def show_settings_window(self):
        """
        Метод для отображения окна настроек.
        """
        from settings import SettingsWindow
        self.settings_window = SettingsWindow(self.current_user)
        self.settings_window.show()
        self.close()

    def show_main_window(self):
        """
        Метод для отображения главного окна.
        """
        from main import MainWindow
        self.main_window = MainWindow(self.current_user)
        self.main_window.show()
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
            song_name=self.song_title,
            artist=self.artist,
            lyrics=self.lyric,
            chords=self.chords
        )

        session.add(saved_song)

        session.commit()
    
    def show_song_details(self):
        """
        Метод для отображения деталей песни.
        """
        if self.song_title and self.chords:
            self.ui.song_label.setText(f"{self.song_title} - {self.artist}\n\nАккорды:\n{self.chords}")
        elif self.song_title and self.lyric:
            self.ui.song_label.setText(f"{self.song_title} - {self.artist}\n\nТекст:\n{self.lyric}")
        else:
            self.ui.song_label.setText("Не удалось определить текст или аккорды песни.")

    def search_text(self):
        """
        Метод для поиска информации о песне по тексту.
        """
        search_text = self.ui.search.text() 
        self.song_title, self.artist, self.lyric, self.chords = find_song_info(search_text)

        if self.song_title:
            self.ui.song_label.setText(f"{self.song_title} - {self.artist}")
        else:
            self.ui.song_label.setText("Не удалось определить название и исполнителя песни.")
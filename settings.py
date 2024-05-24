from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from mydb import session, User, SavedSong

class SettingsWindow(QtWidgets.QMainWindow):
    def __init__(self, current_user):
        super(SettingsWindow, self).__init__()
        self.ui = uic.loadUi('settings.ui', self)
        
        # Подключение сигналов кнопок к соответствующим методам
        self.ui.exit_btn.clicked.connect(self.logout)
        self.ui.return_btn.clicked.connect(self.show_main_window)
        self.ui.to_save_btn.clicked.connect(self.save_user_data)
        self.ui.clear_btn.clicked.connect(self.clear_saved_songs) 
        
        # Установка иконки для окна приложения
        self.setWindowIcon(QIcon('icons/window.png'))

        self.current_user = current_user
        
        # Отображение приветственного сообщения для пользователя
        self.ui.hello.setText(f"Привет, {self.current_user.login}!")
    
    def logout(self):
        """
        Метод для выхода из аккаунта.
        """
        self.current_user = None
        
        from registration import Registration
        self.registration = Registration()
        self.registration.show()
        self.close()
    
    def show_main_window(self):
        """
        Метод для отображения главного окна.
        """
        from main import MainWindow
        self.main_window = MainWindow(self.current_user)
        self.main_window.show()
        self.close()
    
    def clear_saved_songs(self):
        """
        Метод для очистки сохраненных песен пользователя.
        """
        saved_songs = session.query(SavedSong).filter_by(user_id=self.current_user.id).all()

        if saved_songs:
            for song in saved_songs:
                session.delete(song)
            session.commit()
    
    def save_user_data(self):
        """
        Метод для сохранения данных пользователя.
        """
        new_login = self.ui.login.text()
        password = self.ui.password.text()
        gender = self.ui.gender.currentText()

        # Поиск пользователя с таким же ID в базе данных
        existing_user = session.query(User).filter_by(id=self.current_user.id).first()
        
        # Проверка, существует ли пользователь с таким же логином
        user_with_same_login = session.query(User).filter_by(login=new_login).first()
        if user_with_same_login and user_with_same_login.id != existing_user.id:
            return

        # Обновление данных пользователя
        existing_user.login = new_login
        existing_user.password = password
        existing_user.gender = gender
        session.commit()
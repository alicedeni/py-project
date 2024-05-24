import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from mydb import session, User


class Registration(QtWidgets.QMainWindow):
    def __init__(self):
        super(Registration, self).__init__()
        self.ui = uic.loadUi('registration.ui', self)
        
        # Подключение сигналов кнопок к соответствующим методам
        self.ui.enter_btn.clicked.connect(self.check_login)
        self.ui.reg_btn.clicked.connect(self.register_user)
        
        # Установка иконки для окна приложения
        self.setWindowIcon(QIcon('icons/window.png'))

    def check_login(self):
        """
        Метод для проверки логина и пароля пользователя.
        """
        login = self.ui.login.text()
        password = self.ui.password.text()
        
        # Поиск пользователя в базе данных по логину и паролю
        user = session.query(User).filter_by(login=login, password=password).first()
        
        # Проверка, существует ли пользователь с таким логином
        existing_user = session.query(User).filter_by(login=login).first()

        # Если пользователь найден, открывается главное окно приложения
        if user:
            self.current_user = user

            from main import MainWindow
            self.main_window = MainWindow(self.current_user)
            self.main_window.show()
            self.close()
        # Если пользователь с таким логином существует, но пароль неверный
        elif existing_user:
            self.ui.error.setText("Неверный логин или пароль")
        # Если пользователь с таким логином не найден
        else:
            self.ui.error.setText("Пользователь с данным логином не найден")
    
    def register_user(self):
        """
        Метод для регистрации нового пользователя.
        """
        login = self.ui.login.text()
        password = self.ui.password.text()
        
        # Проверка, существует ли пользователь с таким логином
        existing_user = session.query(User).filter_by(login=login).first()
        
        # Если пользователь с таким логином уже существует
        if existing_user:
            self.ui.error.setText("Пользователь с таким логином уже существует")
        # Если пользователь с таким логином не найден, создается новый пользователь
        else:
            new_user = User(login=login, password=password)
            session.add(new_user)
            session.commit()

            self.current_user = new_user
            
            from main import MainWindow
            self.main_window = MainWindow(self.current_user)
            self.main_window.show()
            self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    # Установка иконки для окна приложения
    app.setWindowIcon(QIcon('icons/window.png'))
    
    window = Registration()
    window.show()
    sys.exit(app.exec_())
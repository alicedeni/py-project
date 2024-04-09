import sys
from PyQt5 import QtWidgets, uic

class Registration(QtWidgets.QMainWindow):
    def __init__(self):
        super(Registration, self).__init__()
        self.ui = uic.loadUi('registration.ui', self)
        self.ui.enter_btn.clicked.connect(self.check_login)
        self.ui.reg_btn.clicked.connect(self.check_login)

    def check_login(self):
        if self.ui.login.text() and self.ui.password.text():
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            self.ui.error.setText("Не введены данные для входа")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('main_window.ui', self)
        self.ui.settings_btn.clicked.connect(self.show_settings_window)
        self.ui.search_btn.clicked.connect(self.show_search_window)

    def show_settings_window(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()
        self.close()

    def show_search_window(self):
        self.search_window = SearchWindow()
        self.search_window.show()
        self.close()

class SettingsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.ui = uic.loadUi('settings.ui', self)
        self.ui.exit_btn.clicked.connect(self.register)
        self.ui.return_btn.clicked.connect(self.show_main_window)
    
    def register(self):
        self.registration = Registration()
        self.registration.show()
        self.close()
    
    def show_main_window(self):
        self.search_window = MainWindow()
        self.search_window.show()
        self.close()

class SearchWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SearchWindow, self).__init__()
        self.ui = uic.loadUi('search_window.ui', self)
        self.ui.return_btn.clicked.connect(self.show_main_window)
        self.ui.settings_btn.clicked.connect(self.show_settings_window)

    def show_settings_window(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()
        self.close()

    def show_main_window(self):
        self.search_window = MainWindow()
        self.search_window.show()
        self.close()
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Registration()
    window.show()
    sys.exit(app.exec_())
from PyQt5 import QtWidgets, uic

class SettingsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.ui = uic.loadUi('settings.ui', self)
        self.ui.exit_btn.clicked.connect(self.register)
        self.ui.return_btn.clicked.connect(self.show_main_window)
    
    def register(self):
        from registration import Registration
        self.registration = Registration()
        self.registration.show()
        self.close()
    
    def show_main_window(self):
        from main import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

class SearchWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SearchWindow, self).__init__()
        self.ui = uic.loadUi('search_window.ui', self)
        self.ui.return_btn.clicked.connect(self.show_main_window)
        self.ui.settings_btn.clicked.connect(self.show_settings_window)
        self.setWindowIcon(QIcon('icons/window.png'))

        icon = QIcon()
        icon.addFile("icons/search.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.ui.search_btn.setIcon(icon)

    def show_settings_window(self):
        from settings import SettingsWindow
        self.settings_window = SettingsWindow()
        self.settings_window.show()
        self.close()

    def show_main_window(self):
        from main import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
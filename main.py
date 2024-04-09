from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from settings import SettingsWindow
from search import SearchWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('main_window.ui', self)
        self.ui.settings_btn.clicked.connect(self.show_settings_window)
        self.ui.search_btn.clicked.connect(self.show_search_window)

        icon = QIcon()
        icon.addFile("icons/mic.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.ui.record.setIcon(icon)

    def show_settings_window(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()
        self.close()

    def show_search_window(self):
        self.search_window = SearchWindow()
        self.search_window.show()
        self.close()
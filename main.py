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
        uic.loadUi('main_window.ui', self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Registration()
    window.show()
    sys.exit(app.exec_())
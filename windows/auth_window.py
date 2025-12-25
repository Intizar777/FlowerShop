import sys
from windows.seller_window import SellerWindow
from bd.db_connect import auth
from interface.auth import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox


class AuthWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_enter.clicked.connect(self.on_clicked)
        self.comboBox_role.addItem("Продавец")
        self.comboBox_role.addItem("Клиент")
        self.comboBox_role.addItem("Менеджер")

    def on_clicked(self):
        login = self.lineEdit_login.text()
        passw = self.lineEdit_passw.text()
        role_name = self.comboBox_role.currentText()
        res = auth(login, passw, role_name)
        if res is None:
            QMessageBox.setText("Ошибка: Введите корректные данные")
        else:
            self.win = SellerWindow()
            self.win.show()
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())
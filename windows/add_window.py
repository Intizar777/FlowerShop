from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QMessageBox

from interface.dialog_add import Ui_Dialog

class AddDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_save.clicked.connect(self.on_save)

    def on_save(self):
        name = self.lineEdit_name.text()
        surname = self.lineEdit_surname.text()
        email = self.lineEdit_email.text()
        if not name or not surname or not email:
            QMessageBox.warning(self, "Ты че бл данные вводить не умеешь?", "Бро, вводим текст корректно, ок.")
        else:
            self.accept()





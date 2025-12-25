import sys
from windows.add_window import AddDialog
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QStandardItem, QStandardItemModel

from interface.seller import Ui_MainWindow
from bd.db_connect import *
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableView, QInputDialog


class SellerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.proxy = QtCore.QSortFilterProxyModel()
        self.proxy.setFilterKeyColumn(1)
        self.load_info()
        self.lineEdit_fio_cl.textChanged.connect(self.proxy.setFilterFixedString)
        self.pushButton_edit_cl.clicked.connect(self.edit)
        self.pushButton_delete_cl.clicked.connect(self.delete)
        self.pushButton_add_cl.clicked.connect(self.add)


    def load_info(self):
        self.data = get_data()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["id", "Имя", "Фамилия", "E-mail"])

        self.columns = ["id", "name", "surname", "email"]
        for row in self.data:
            items = [QStandardItem(str(val)) for col, val in row.items() if col in self.columns]

            self.model.appendRow(items)
        self.proxy.setSourceModel(self.model)
        self.tableView.setModel(self.proxy)

    def edit(self):
        model = self.tableView.model().sourceModel()
        rows = model.rowCount()
        for i in range(rows):
            id = int(model.item(i, 0).text())
            name = model.item(i, 1).text()
            surname = model.item(i, 2).text()
            email = model.item(i, 3).text()
            res = update_client(name, surname, email, id)
            if not res["success"]:
                QMessageBox.warning(self, "Ошибка", "Ошибка братик")
                return
        else:
            QMessageBox.information(self, "Успех", "Все нормально, двигаемся дальше, работаем с этим, мы можем с этим поработать")

    def delete(self):
        value, ok = QInputDialog.getInt(self, "Удаление", "Введите ID клиента", min=1)
        if ok == True:
            delete_cl = delete_client(value)
            if not delete_cl["success"]:
                QMessageBox.warning(self, "Ошибка", "Ошибка братик")
            else:
                QMessageBox.information(self, "Успех", "Норм все")
                self.load_info()

    def add(self):
        win_dig = AddDialog()
        if win_dig.exec():
            name = win_dig.lineEdit_name.text()
            surname = win_dig.lineEdit_surname.text()
            email = win_dig.lineEdit_email.text()
            addd = add_client(name, surname, email)
            if not addd["success"]:
                QMessageBox.warning(self, "Ошибка", "Ошибка братик")
            else:
                QMessageBox.information(self, "Успех", "Норм все")
                self.load_info()

if __name__ =="__main__":
    app = QApplication(sys.argv)
    start_window = SellerWindow()
    start_window.show()
    sys.exit(app.exec())

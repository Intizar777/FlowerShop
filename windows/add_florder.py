import sys

from interface.add_florder import Ui_Dialog
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QStandardItem, QStandardItemModel

from bd.db_connect import *
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog, QTableView, QInputDialog, QMessageBox


class OrderWindow(QDialog, Ui_Dialog):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.user_id = user_id
        self.pushButton_order_buy.clicked.connect(self.on_save_ord)
        self.load_products()

        self.spinBox_quan.valueChanged.connect(self.calculate_price)
        self.comboBox_buy.currentIndexChanged.connect(self.calculate_price)


    def load_products(self):
        products = get_data_products()
        for product in products:
            self.comboBox_buy.addItem(product['prod_name'])

    def calculate_price(self):
        try:
            selected_name = self.comboBox_buy.currentText()
            products = get_data_products()

            for product in products:
                if product['prod_name'] == selected_name:
                    price = float(product['price'])
                    quantity = self.spinBox_quan.value()
                    total = price * quantity
                    self.lineEdit_orice.setText(f"{total:.2f}")
                    break
        except:
            pass

    def on_save_ord(self):
        try:
            quantity = self.spinBox_quan.value()
            total_price = float(self.lineEdit_orice.text())

            if quantity <= 0:
                QMessageBox.warning(self, "Ошибка", "Укажите количество!")
                return

            result = add_order(total_price)  # Только сумма

            if result["success"]:
                QMessageBox.information(self, "Успех", "Заказ оформлен!")
                self.accept()
            else:
                QMessageBox.warning(self, "Ошибка", result['message'])

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrderWindow()
    window.show()
    sys.exit(app.exec())
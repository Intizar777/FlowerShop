import sys
from PyQt6 import QtCore
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox

from interface.client import Ui_MainWindow
from windows.add_florder import OrderWindow
from bd.db_connect import *


class ClientWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, user_id=None):
        super().__init__()
        self.setupUi(self)
        self.user_id = user_id
        self.proxy = QtCore.QSortFilterProxyModel()
        self.proxy.setFilterKeyColumn(1)

        self.proxy_orders = QtCore.QSortFilterProxyModel()

        self.load_info_flowers()
        self.load_info_orders()  # Загружаем заказы при запуске

        # Подключаем сигналы
        self.lineEdit_flo.textChanged.connect(self.proxy.setFilterFixedString)
        self.pushButton_find_ord.clicked.connect(self.filter_orders)  # Кнопка "Найти"
        self.pushButton_add_fl.clicked.connect(self.add_fl)

    def load_info_orders(self):
        """Загрузка заказов в таблицу"""
        self.orders_data = get_data_orders(user_id=self.user_id)  # Все заказы

        # Создаем модель для заказов
        self.model_orders = QStandardItemModel()
        self.model_orders.setHorizontalHeaderLabels(["Дата заказа", "Сумма", "Статус"])

        for row in self.orders_data:
            # Форматируем дату
            date_val = row.get('order_date', '')
            if date_val:
                date_val = date_val.strftime('%Y-%m-%d')

            # Получаем сумму и статус
            amount = row.get('total_amount', '0')
            status = row.get('status', '')

            items = [
                QStandardItem(str(date_val)),
                QStandardItem(str(amount)),
                QStandardItem(str(status))
            ]
            self.model_orders.appendRow(items)

        self.tableView_2.setModel(self.model_orders)

    def filter_orders(self):
        """Фильтр заказов по дате"""
        filter_date = self.lineEdit_date.text()

        # Получаем отфильтрованные или все заказы
        if filter_date:
            self.orders_data = get_data_orders(filter_date, self.user_id)
        else:
            self.orders_data = get_data_orders(user_id=self.user_id)

        self.update_orders_table()

    def update_orders_table(self):
        """Обновить таблицу заказов"""
        self.model_orders = QStandardItemModel()
        self.model_orders.clear()
        self.model_orders.setHorizontalHeaderLabels(["Дата заказа", "Сумма", "Статус"])

        for row in self.orders_data:
            date_val = row.get('order_date', '')
            if date_val:
                date_val = date_val.strftime('%Y-%m-%d')

            amount = row.get('total_amount', '0')
            status = row.get('status', '')

            items = [
                QStandardItem(str(date_val)),
                QStandardItem(str(amount)),
                QStandardItem(str(status))
            ]
            self.model_orders.appendRow(items)

        self.tableView_2.setModel(self.model_orders)

    def load_info_flowers(self):
        """Загрузка товаров в каталог"""
        self.data = get_data_products()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["id", "Товар", "Цена", "ед.изм."])

        self.columns = ["id", "prod_name", "price", "units"]
        for row in self.data:
            items = [QStandardItem(str(val)) for col, val in row.items() if col in self.columns]
            self.model.appendRow(items)

        self.proxy.setSourceModel(self.model)
        self.tableView_flowers.setModel(self.proxy)

    def add_fl(self):
        """Добавить заказ"""
        win_dialog = OrderWindow(user_id=self.user_id)
        if win_dialog.exec():
            QMessageBox.information(self, "Успех", "Заказ оформлен!")
            # После оформления обновляем таблицу заказов
            self.load_info_orders()
        else:
            QMessageBox.information(self, "Информация", "Оформление заказа отменено")

    def count_price(self, price_per_one, quantity):
        return price_per_one * quantity


if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_window = ClientWindow()
    start_window.show()
    sys.exit(app.exec())
CREATE DATABASE flower_shop;

USE flower_shop;

CREATE TABLE roles(id INT PRIMARY KEY AUTO_INCREMENT, role VARCHAR(100));
INSERT INTO roles(role) VALUES ("продавец"), ("клиент"), ("менеджер");

CREATE TABLE users(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100), surname VARCHAR(100), role_id INT,
email VARCHAR(200), passw VARCHAR(100), FOREIGN KEY(role_id) REFERENCES roles(id));
INSERT INTO users(name, surname, role_id, email, passw)
VALUES ("Мария", "Сидорова", 1, "maria@shop.ru", "ekthW14t"),
("Иван", "Иванов", 2, "ivan@example.com", "ewN31lkq"),
("Сергей", "Кузнецов", 3, "sergey@shop.ru", "rDti21eM");

CREATE TABLE prod_cat(id INT PRIMARY KEY AUTO_INCREMENT, cat_name VARCHAR(100));
INSERT INTO prod_cat(cat_name)
VALUES ("букеты"), ("цветы"), ("упаковка"), ("открытки");

CREATE TABLE products(id INT PRIMARY KEY AUTO_INCREMENT, prod_name VARCHAR(100), cat_id INT,
price DECIMAL(10,2), units VARCHAR(50), FOREIGN KEY(cat_id) REFERENCES prod_cat(id));
INSERT INTO products(prod_name, cat_id, price, units) VALUES ("Роза Красная", 1, 150, "шт"),
("Букет Весенний", 2, 2500, "букет"), ("Крафт-бумага", 3, 50, "рулон");

CREATE TABLE inventory(id INT PRIMARY KEY AUTO_INCREMENT, prod_id INT,
quan_in_stock INT, min_quan INT, last_restock_date DATE, FOREIGN KEY(prod_id) REFERENCES products(id));
INSERT INTO inventory(prod_id, quan_in_stock, min_quan, last_restock_date) VALUES (1, 200, 50, "2025-12-15"),
(2, 15, 10, "2025-12-10"),
(3, 100, 20, "2025-12-1");

CREATE TABLE orders(id INT PRIMARY KEY AUTO_INCREMENT, user_id INT,
order_date DATE, delivery_date DATE, status VARCHAR(50),
total_amount DECIMAL(10, 2), FOREIGN KEY (user_id) REFERENCES users(id));

INSERT INTO orders(user_id, order_date, delivery_date, status, total_amount)
VALUES(1, "2025-12-20", "2025-12-21", "Принят", NULL), (1, "2025-12-19", "2025-12-20", "В обработке", NULL);

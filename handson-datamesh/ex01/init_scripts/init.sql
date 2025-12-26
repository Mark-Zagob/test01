-- init_scripts/init.sql

-- 1. Tạo Schema cho Products Domain (Team Sản Phẩm)
CREATE SCHEMA IF NOT EXISTS products_domain;

CREATE TABLE products_domain.raw_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10, 2)
);

-- Dữ liệu giả cho Products
INSERT INTO products_domain.raw_items (name, category, price) VALUES
('iPhone 15', 'Electronics', 999.00),
('Samsung S24', 'Electronics', 899.00),
('T-Shirt', 'Clothing', 15.00);


-- 2. Tạo Schema cho Orders Domain (Team Đơn Hàng)
CREATE SCHEMA IF NOT EXISTS orders_domain;

CREATE TABLE orders_domain.raw_transactions (
    id SERIAL PRIMARY KEY,
    product_id INT,
    quantity INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dữ liệu giả cho Orders
INSERT INTO orders_domain.raw_transactions (product_id, quantity) VALUES
(1, 2), -- Mua 2 iPhone
(3, 10); -- Mua 10 cái áo

-- Chèn thêm một dữ liệu sai (Giá bị âm)
INSERT INTO products_domain.raw_items (name, category, price) 
VALUES ('Lỗi Đánh Máy', 'Electronics', -500.00);

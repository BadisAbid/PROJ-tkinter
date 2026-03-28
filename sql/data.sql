-- Sample Data for Smart Management System

USE smart_management_system;

-- Sample Categories
INSERT INTO categories (name, description) VALUES 
('Electronics', 'Devices and gadgets'),
('Clothing', 'Apparel and accessories'),
('Home & Kitchen', 'Home appliances and kitchenware');

-- Sample Products
INSERT INTO products (category_id, name, price, stock) VALUES 
(1, 'Laptop Pro', 1200.00, 15),
(1, 'Smartphone X', 800.00, 30),
(2, 'Cotton T-Shirt', 25.00, 100),
(3, 'Coffee Maker', 60.00, 20);

-- Sample Orders
INSERT INTO orders (product_id, customer_name, quantity, total_price) VALUES 
(1, 'Alice Smith', 1, 1200.00),
(3, 'Bob Johnson', 2, 50.00);

-- Sample User
INSERT INTO users (username, password) VALUES ('admin', 'admin123');

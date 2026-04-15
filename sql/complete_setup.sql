-- Complete Database Setup for Smart Management System
-- This script creates the database, tables, and loads all sample data

CREATE DATABASE IF NOT EXISTS smart_management_system;
USE smart_management_system;

-- ===== TABLE CREATION =====

-- Table 1: Categories
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
) ENGINE=InnoDB;

-- Table 2: Products
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    stock INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Table 3: Orders
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    total_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Table 4: Users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;


-- Default Admin User (password: admin123 - hashed SHA256)
INSERT IGNORE INTO users (username, email, password) VALUES 
('admin', 'admin@supermarket.local', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9');

-- Sample Supermarket Categories
INSERT IGNORE INTO categories (name, description) VALUES 
('Fruits & Vegetables', 'Fresh produce section'),
('Dairy & Eggs', 'Milk, cheese, yogurt, and eggs'),
('Meat & Seafood', 'Fresh meat, poultry, and seafood'),
('Bakery', 'Bread, pastries, and baked goods'),
('Beverages', 'Coffee, tea, juice, and soft drinks'),
('Pantry Staples', 'Rice, pasta, flour, and grains'),
('Snacks & Sweets', 'Chips, cookies, and confectionery'),
('Frozen Foods', 'Frozen vegetables, meals, and ice cream'),
('Personal Care', 'Soap, shampoo, toothpaste'),
('Household Items', 'Cleaning supplies and essentials');

-- Fruits & Vegetables Products (10 items)
INSERT IGNORE INTO products (category_id, name, price, stock) VALUES 
(1, 'Fresh Apples', 3.99, 150),
(1, 'Organic Bananas', 2.49, 200),
(1, 'Carrots (1kg)', 1.99, 100),
(1, 'Broccoli', 3.49, 85),
(1, 'Tomatoes', 4.99, 120),
(1, 'Lettuce (Head)', 2.99, 95),
(1, 'Bell Peppers (Red)', 5.99, 70),
(1, 'Potatoes (5kg)', 8.99, 60),
(1, 'Onions (3kg)', 5.49, 80),
(1, 'Mixed Berries (500g)', 6.99, 45);

-- Dairy & Eggs Products (10 items)
INSERT IGNORE INTO products (category_id, name, price, stock) VALUES 
(2, 'Whole Milk (1L)', 3.29, 200),
(2, 'Cheddar Cheese', 7.99, 85),
(2, 'Greek Yogurt (500g)', 5.49, 110),
(2, 'Eggs (Dozen)', 4.99, 250),
(2, 'Butter (500g)', 6.99, 75),
(2, 'Cream Cheese', 4.99, 60),
(2, 'Mozzarella Cheese', 8.49, 70),
(2, 'Low-Fat Milk (1L)', 2.99, 180),
(2, 'Sour Cream (500ml)', 3.99, 55),
(2, 'Feta Cheese', 7.49, 50);

-- Meat & Seafood Products (10 items)
INSERT IGNORE INTO products (category_id, name, price, stock) VALUES 
(3, 'Chicken Breast (1kg)', 9.99, 120),
(3, 'Ground Beef (500g)', 8.49, 95),
(3, 'Salmon Fillet (500g)', 14.99, 45),
(3, 'Pork Chops (500g)', 7.99, 70),
(3, 'Turkey Breast', 11.99, 55),
(3, 'Shrimp (500g)', 16.99, 40),
(3, 'Lamb Chops', 13.99, 35),
(3, 'Bacon (500g)', 6.99, 85),
(3, 'Sausages (500g)', 5.99, 100),
(3, 'Cod Fillet', 12.99, 50);

-- Bakery Products (10 items)
INSERT IGNORE INTO products (category_id, name, price, stock) VALUES 
(4, 'Whole Wheat Bread', 3.49, 60),
(4, 'Croissants (4-pack)', 5.99, 50),
(4, 'Bagels (6-pack)', 4.99, 45),
(4, 'Ciabatta Bread', 4.49, 35),
(4, 'Sourdough Loaf', 5.99, 40),
(4, 'Blueberry Muffins', 6.99, 30),
(4, 'Chocolate Chip Cookies', 4.99, 70),
(4, 'Baguette', 3.99, 50),
(4, 'Multigrain Bread', 4.49, 55),
(4, 'Donut Mix (6-pack)', 5.49, 40);

-- Beverages Products (10 items)
INSERT IGNORE INTO products (category_id, name, price, stock) VALUES 
(5, 'Orange Juice (1L)', 4.49, 100),
(5, 'Coffee Beans (500g)', 8.99, 75),
(5, 'Green Tea (20-pack)', 5.99, 60),
(5, 'Coca Cola (2L)', 3.99, 150),
(5, 'Water Bottles (24-pack)', 4.99, 200),
(5, 'Apple Juice (1L)', 3.99, 85),
(5, 'Iced Coffee', 3.49, 120),
(5, 'Energy Drink (24oz)', 2.99, 110),
(5, 'Lemonade (2L)', 3.49, 95),
(5, 'Sparkling Water (6-pack)', 5.99, 80);

-- Pantry Staples Products (10 items)
INSERT IGNORE INTO products (category_id, name, price, stock) VALUES 
(6, 'Jasmine Rice (2kg)', 6.99, 100),
(6, 'Pasta (500g)', 1.99, 250),
(6, 'Olive Oil (1L)', 9.99, 50),
(6, 'All-Purpose Flour (2kg)', 3.99, 120),
(6, 'Peanut Butter (500g)', 4.99, 85),
(6, 'Canned Beans (400g)', 1.99, 200),
(6, 'Tomato Sauce (500ml)', 2.49, 150),
(6, 'Sugar (2kg)', 3.99, 100),
(6, 'Cornflakes Cereal', 4.99, 70),
(6, 'Honey (500ml)', 8.99, 45);

-- Snacks & Sweets Products (10 items)
INSERT IGNORE INTO products (category_id, name, price, stock) VALUES 
(7, 'Potato Chips (200g)', 3.49, 120),
(7, 'Chocolate Bars (pack)', 7.99, 200),
(7, 'Pretzels (400g)', 4.99, 95),
(7, 'Granola Bars (12-pack)', 9.99, 85),
(7, 'Gummy Bears (500g)', 5.99, 110),
(7, 'Popcorn (microwave)', 4.49, 100),
(7, 'Mixed Nuts (300g)', 8.99, 60),
(7, 'Crackers (300g)', 3.99, 130),
(7, 'Candy Mix (1kg)', 9.99, 50),
(7, 'Trail Mix (400g)', 6.99, 75);

-- Frozen Foods Products (10 items)
INSERT IGNORE INTO products (category_id, name, price, stock) VALUES 
(8, 'Frozen Pizza (3-pack)', 12.99, 80),
(8, 'Frozen Vegetables Mix', 3.99, 140),
(8, 'Ice Cream (2L)', 7.99, 100),
(8, 'Frozen Fries (1kg)', 4.99, 110),
(8, 'Frozen Berries (600g)', 5.99, 90),
(8, 'Frozen Dinner (5-pack)', 14.99, 60),
(8, 'Frozen Broccoli (400g)', 2.99, 120),
(8, 'Frozen Shrimp (400g)', 10.99, 45),
(8, 'Popsicles (12-pack)', 4.99, 150),
(8, 'Frozen Waffles (24-pack)', 5.99, 85);

-- Personal Care Products (10 items)
INSERT IGNORE INTO products (category_id, name, price, stock) VALUES 
(9, 'Shampoo (500ml)', 6.99, 85),
(9, 'Conditioner (500ml)', 6.99, 75),
(9, 'Toothpaste (100ml)', 3.99, 150),
(9, 'Soap Bars (6-pack)', 5.99, 100),
(9, 'Deodorant', 4.99, 120),
(9, 'Face Wash (200ml)', 7.99, 70),
(9, 'Lotion (250ml)', 8.99, 60),
(9, 'Toothbrush (2-pack)', 4.49, 110),
(9, 'Hair Gel (200ml)', 5.99, 50),
(9, 'Mouthwash (500ml)', 4.99, 90);

-- Household Items Products (10 items)
INSERT IGNORE INTO products (category_id, name, price, stock) VALUES 
(10, 'Laundry Detergent (2L)', 9.99, 80),
(10, 'Dish Soap (500ml)', 2.99, 150),
(10, 'Paper Towels (12-roll)', 11.99, 70),
(10, 'Toilet Paper (12-roll)', 14.99, 120),
(10, 'Glass Cleaner (500ml)', 3.99, 90),
(10, 'All-Purpose Cleaner', 3.49, 110),
(10, 'Trash Bags (50-count)', 6.99, 100),
(10, 'Sponges (5-pack)', 2.99, 140),
(10, 'Bleach (1L)', 3.99, 75),
(10, 'Disinfectant Wipes (100-pack)', 5.99, 130);

-- Sample Transactions (15 orders)
INSERT IGNORE INTO orders (product_id, customer_name, quantity, total_price) VALUES 
(1, 'John Smith', 5, 19.95),
(2, 'Emma Wilson', 3, 7.47),
(15, 'Michael Brown', 2, 8.98),
(10, 'Sarah Davis', 1, 4.99),
(25, 'James Johnson', 2, 27.98),
(35, 'Lisa Anderson', 4, 23.96),
(42, 'Robert Taylor', 2, 10.98),
(58, 'Jennifer White', 3, 14.97),
(72, 'David Miller', 1, 6.99),
(89, 'Mary Martinez', 5, 29.95),
(5, 'Chris Evans', 2, 9.98),
(20, 'Patricia Garcia', 1, 3.99),
(45, 'Richard Lewis', 3, 14.97),
(65, 'Jessica Rodriguez', 2, 11.98),
(80, 'Thomas Anderson', 4, 23.96);

-- ===== COMPLETION =====
-- Database setup complete!
-- Total: 1 database, 4 tables, 1 admin user, 10 categories, 100 products, 15 sample orders

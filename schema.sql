-- Create the database
CREATE DATABASE IF NOT EXISTS restaurant_db;
USE restaurant_db;

-- Create table for menu items
CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category ENUM('Fast Food', 'Desi Food', 'Beverage') NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    image_path VARCHAR(255)
);

-- Create table for customer orders
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    total DECIMAL(10,2),
    includes_beverage BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table for order items
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    item_id INT,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES menu_items(id) ON DELETE CASCADE
);

-- Create table for customer reviews
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create admin user table
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Insert default admin credentials (username: admin, password: admin123)
INSERT IGNORE INTO admin_users (username, password)
VALUES ('admin', 'admin123');

-- Sample data for menu
INSERT INTO menu_items (name, category, price, image_path) VALUES
('Chicken Burger', 'Fast Food', 250.00, 'images/chickenburger.jpg'),
('Beef Burger', 'Fast Food', 300.00, 'images/beefburger.jpg'),
('Zinger Burger', 'Fast Food', 300.00, 'images/zingerburger.jpg'),
('Chest Fried Chicken', 'Fast Food', 300.00, 'images/chestfriedchicken.jpg'),
('Leg Fried Chicken', 'Fast Food', 260.00, 'images/slegfriedchicken.jpg'),
('Regular Pepsi', 'Beverage', 100.00, 'images/pepsi.jpg'),
('Regular Miranda', 'Beverage', 100.00, 'images/miranda.jpg'),
('Regular Sprite', 'Beverage', 100.00, 'images/sprite.jpg'),
('Chicken Karhai', 'Desi Food', 250.00, 'images/chickenkarhai.jpg'),
('Chicken Korma', 'Desi Food', 300.00, 'images/chickenkorma.jpg'),
('Bun Kebab', 'Desi Food', 120.00, 'images/bunkebab.jpg'),
('Pulao', 'Desi Food', 150.00, 'images/pulao.jpg'),
('Biryani', 'Desi Food', 170.00, 'images/biryani.jpg'),
('Nihari', 'Desi Food', 200.00, 'images/nihari.jpg');

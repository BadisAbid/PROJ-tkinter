"""
Smart Management System - Database Loader
Loads comprehensive supermarket data into the database
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import hashlib

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_supermarket_data():
    """Load supermarket products and categories into database"""
    
    try:
        # Connect to database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("=" * 60)
        print("Smart Management System - Database Loader")
        print("=" * 60)
        print()
        
        # Clear existing data (optional - uncomment to reset)
        # print("Clearing existing data...")
        # cursor.execute("DELETE FROM orders")
        # cursor.execute("DELETE FROM products")
        # cursor.execute("DELETE FROM categories")
        # cursor.execute("DELETE FROM users WHERE username != 'admin'")
        # connection.commit()
        
        # 1. Create Admin User
        print("✓ Creating admin user...")
        admin_password = hash_password('admin123')
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                ('admin', 'admin@supermarket.local', admin_password)
            )
            connection.commit()
            print("  ✅ Admin user created")
        except Error:
            print("  ℹ️  Admin user already exists")
        
        # 2. Create Categories
        print("\n✓ Creating categories...")
        categories_data = [
            ('Fruits & Vegetables', 'Fresh produce section'),
            ('Dairy & Eggs', 'Milk, cheese, yogurt, and eggs'),
            ('Meat & Seafood', 'Fresh meat, poultry, and seafood'),
            ('Bakery', 'Bread, pastries, and baked goods'),
            ('Beverages', 'Coffee, tea, juice, and soft drinks'),
            ('Pantry Staples', 'Rice, pasta, flour, and grains'),
            ('Snacks & Sweets', 'Chips, cookies, and confectionery'),
            ('Frozen Foods', 'Frozen vegetables, meals, and ice cream'),
            ('Personal Care', 'Soap, shampoo, toothpaste'),
            ('Household Items', 'Cleaning supplies and essentials')
        ]
        
        for name, description in categories_data:
            try:
                cursor.execute(
                    "INSERT INTO categories (name, description) VALUES (%s, %s)",
                    (name, description)
                )
            except Error:
                pass  # Category might already exist
        
        connection.commit()
        print(f"  ✅ {len(categories_data)} categories ready")
        
        # 3. Get category IDs
        cursor.execute("SELECT id, name FROM categories")
        categories = {row[1]: row[0] for row in cursor.fetchall()}
        
        # 4. Insert Products
        print("\n✓ Creating products...")
        
        products_data = [
            # Fruits & Vegetables
            ('Fruits & Vegetables', 'Fresh Apples', 3.99, 150),
            ('Fruits & Vegetables', 'Organic Bananas', 2.49, 200),
            ('Fruits & Vegetables', 'Carrots (1kg)', 1.99, 100),
            ('Fruits & Vegetables', 'Broccoli', 3.49, 85),
            ('Fruits & Vegetables', 'Tomatoes', 4.99, 120),
            ('Fruits & Vegetables', 'Lettuce (Head)', 2.99, 95),
            ('Fruits & Vegetables', 'Bell Peppers (Red)', 5.99, 70),
            ('Fruits & Vegetables', 'Potatoes (5kg)', 8.99, 60),
            ('Fruits & Vegetables', 'Onions (3kg)', 5.49, 80),
            ('Fruits & Vegetables', 'Mixed Berries (500g)', 6.99, 45),
            
            # Dairy & Eggs
            ('Dairy & Eggs', 'Whole Milk (1L)', 3.29, 200),
            ('Dairy & Eggs', 'Cheddar Cheese', 7.99, 85),
            ('Dairy & Eggs', 'Greek Yogurt (500g)', 5.49, 110),
            ('Dairy & Eggs', 'Eggs (Dozen)', 4.99, 250),
            ('Dairy & Eggs', 'Butter (500g)', 6.99, 75),
            ('Dairy & Eggs', 'Cream Cheese', 4.99, 60),
            ('Dairy & Eggs', 'Mozzarella Cheese', 8.49, 70),
            ('Dairy & Eggs', 'Low-Fat Milk (1L)', 2.99, 180),
            ('Dairy & Eggs', 'Sour Cream (500ml)', 3.99, 55),
            ('Dairy & Eggs', 'Feta Cheese', 7.49, 50),
            
            # Meat & Seafood
            ('Meat & Seafood', 'Chicken Breast (1kg)', 9.99, 120),
            ('Meat & Seafood', 'Ground Beef (500g)', 8.49, 95),
            ('Meat & Seafood', 'Salmon Fillet (500g)', 14.99, 45),
            ('Meat & Seafood', 'Pork Chops (500g)', 7.99, 70),
            ('Meat & Seafood', 'Turkey Breast', 11.99, 55),
            ('Meat & Seafood', 'Shrimp (500g)', 16.99, 40),
            ('Meat & Seafood', 'Lamb Chops', 13.99, 35),
            ('Meat & Seafood', 'Bacon (500g)', 6.99, 85),
            ('Meat & Seafood', 'Sausages (500g)', 5.99, 100),
            ('Meat & Seafood', 'Cod Fillet', 12.99, 50),
            
            # Bakery
            ('Bakery', 'Whole Wheat Bread', 3.49, 60),
            ('Bakery', 'Croissants (4-pack)', 5.99, 50),
            ('Bakery', 'Bagels (6-pack)', 4.99, 45),
            ('Bakery', 'Ciabatta Bread', 4.49, 35),
            ('Bakery', 'Sourdough Loaf', 5.99, 40),
            ('Bakery', 'Blueberry Muffins', 6.99, 30),
            ('Bakery', 'Chocolate Chip Cookies', 4.99, 70),
            ('Bakery', 'Baguette', 3.99, 50),
            ('Bakery', 'Multigrain Bread', 4.49, 55),
            ('Bakery', 'Donut Mix (6-pack)', 5.49, 40),
            
            # Beverages
            ('Beverages', 'Orange Juice (1L)', 4.49, 100),
            ('Beverages', 'Coffee Beans (500g)', 8.99, 75),
            ('Beverages', 'Green Tea (20-pack)', 5.99, 60),
            ('Beverages', 'Coca Cola (2L)', 3.99, 150),
            ('Beverages', 'Water Bottles (24-pack)', 4.99, 200),
            ('Beverages', 'Apple Juice (1L)', 3.99, 85),
            ('Beverages', 'Iced Coffee', 3.49, 120),
            ('Beverages', 'Energy Drink (24oz)', 2.99, 110),
            ('Beverages', 'Lemonade (2L)', 3.49, 95),
            ('Beverages', 'Sparkling Water (6-pack)', 5.99, 80),
            
            # Pantry Staples
            ('Pantry Staples', 'Jasmine Rice (2kg)', 6.99, 100),
            ('Pantry Staples', 'Pasta (500g)', 1.99, 250),
            ('Pantry Staples', 'Olive Oil (1L)', 9.99, 50),
            ('Pantry Staples', 'All-Purpose Flour (2kg)', 3.99, 120),
            ('Pantry Staples', 'Peanut Butter (500g)', 4.99, 85),
            ('Pantry Staples', 'Canned Beans (400g)', 1.99, 200),
            ('Pantry Staples', 'Tomato Sauce (500ml)', 2.49, 150),
            ('Pantry Staples', 'Sugar (2kg)', 3.99, 100),
            ('Pantry Staples', 'Cornflakes Cereal', 4.99, 70),
            ('Pantry Staples', 'Honey (500ml)', 8.99, 45),
            
            # Snacks & Sweets
            ('Snacks & Sweets', 'Potato Chips (200g)', 3.49, 120),
            ('Snacks & Sweets', 'Chocolate Bars (pack)', 7.99, 200),
            ('Snacks & Sweets', 'Pretzels (400g)', 4.99, 95),
            ('Snacks & Sweets', 'Granola Bars (12-pack)', 9.99, 85),
            ('Snacks & Sweets', 'Gummy Bears (500g)', 5.99, 110),
            ('Snacks & Sweets', 'Popcorn (microwave)', 4.49, 100),
            ('Snacks & Sweets', 'Mixed Nuts (300g)', 8.99, 60),
            ('Snacks & Sweets', 'Crackers (300g)', 3.99, 130),
            ('Snacks & Sweets', 'Candy Mix (1kg)', 9.99, 50),
            ('Snacks & Sweets', 'Trail Mix (400g)', 6.99, 75),
            
            # Frozen Foods
            ('Frozen Foods', 'Frozen Pizza (3-pack)', 12.99, 80),
            ('Frozen Foods', 'Frozen Vegetables Mix', 3.99, 140),
            ('Frozen Foods', 'Ice Cream (2L)', 7.99, 100),
            ('Frozen Foods', 'Frozen Fries (1kg)', 4.99, 110),
            ('Frozen Foods', 'Frozen Berries (600g)', 5.99, 90),
            ('Frozen Foods', 'Frozen Dinner (5-pack)', 14.99, 60),
            ('Frozen Foods', 'Frozen Broccoli (400g)', 2.99, 120),
            ('Frozen Foods', 'Frozen Shrimp (400g)', 10.99, 45),
            ('Frozen Foods', 'Popsicles (12-pack)', 4.99, 150),
            ('Frozen Foods', 'Frozen Waffles (24-pack)', 5.99, 85),
            
            # Personal Care
            ('Personal Care', 'Shampoo (500ml)', 6.99, 85),
            ('Personal Care', 'Conditioner (500ml)', 6.99, 75),
            ('Personal Care', 'Toothpaste (100ml)', 3.99, 150),
            ('Personal Care', 'Soap Bars (6-pack)', 5.99, 100),
            ('Personal Care', 'Deodorant', 4.99, 120),
            ('Personal Care', 'Face Wash (200ml)', 7.99, 70),
            ('Personal Care', 'Lotion (250ml)', 8.99, 60),
            ('Personal Care', 'Toothbrush (2-pack)', 4.49, 110),
            ('Personal Care', 'Hair Gel (200ml)', 5.99, 50),
            ('Personal Care', 'Mouthwash (500ml)', 4.99, 90),
            
            # Household Items
            ('Household Items', 'Laundry Detergent (2L)', 9.99, 80),
            ('Household Items', 'Dish Soap (500ml)', 2.99, 150),
            ('Household Items', 'Paper Towels (12-roll)', 11.99, 70),
            ('Household Items', 'Toilet Paper (12-roll)', 14.99, 120),
            ('Household Items', 'Glass Cleaner (500ml)', 3.99, 90),
            ('Household Items', 'All-Purpose Cleaner', 3.49, 110),
            ('Household Items', 'Trash Bags (50-count)', 6.99, 100),
            ('Household Items', 'Sponges (5-pack)', 2.99, 140),
            ('Household Items', 'Bleach (1L)', 3.99, 75),
            ('Household Items', 'Disinfectant Wipes (100-pack)', 5.99, 130),
        ]
        
        product_count = 0
        for category_name, product_name, price, stock in products_data:
            try:
                category_id = categories[category_name]
                cursor.execute(
                    "INSERT INTO products (category_id, name, price, stock) VALUES (%s, %s, %s, %s)",
                    (category_id, product_name, price, stock)
                )
                product_count += 1
            except Error as e:
                print(f"  ⚠️  Error inserting {product_name}: {e}")
        
        connection.commit()
        print(f"  ✅ {product_count} products created")
        
        # 5. Insert Sample Orders
        print("\n✓ Creating sample orders...")
        
        # Get product IDs
        cursor.execute("SELECT id FROM products ORDER BY RAND() LIMIT 15")
        product_ids = [row[0] for row in cursor.fetchall()]
        
        orders_data = [
            (product_ids[0] if len(product_ids) > 0 else 1, 'John Smith', 5, 19.95),
            (product_ids[1] if len(product_ids) > 1 else 2, 'Emma Wilson', 3, 7.47),
            (product_ids[2] if len(product_ids) > 2 else 3, 'Michael Brown', 2, 8.98),
            (product_ids[3] if len(product_ids) > 3 else 4, 'Sarah Davis', 1, 4.99),
            (product_ids[4] if len(product_ids) > 4 else 5, 'James Johnson', 2, 27.98),
            (product_ids[5] if len(product_ids) > 5 else 6, 'Lisa Anderson', 4, 23.96),
            (product_ids[6] if len(product_ids) > 6 else 7, 'Robert Taylor', 2, 10.98),
            (product_ids[7] if len(product_ids) > 7 else 8, 'Jennifer White', 3, 14.97),
            (product_ids[8] if len(product_ids) > 8 else 9, 'David Miller', 1, 6.99),
            (product_ids[9] if len(product_ids) > 9 else 10, 'Mary Martinez', 5, 29.95),
            (product_ids[10] if len(product_ids) > 10 else 11, 'Chris Evans', 2, 9.98),
            (product_ids[11] if len(product_ids) > 11 else 12, 'Patricia Garcia', 1, 3.99),
            (product_ids[12] if len(product_ids) > 12 else 13, 'Richard Lewis', 3, 14.97),
            (product_ids[13] if len(product_ids) > 13 else 14, 'Jessica Rodriguez', 2, 11.98),
            (product_ids[14] if len(product_ids) > 14 else 15, 'Thomas Anderson', 4, 23.96),
        ]
        
        order_count = 0
        for product_id, customer_name, quantity, total_price in orders_data:
            try:
                cursor.execute(
                    "INSERT INTO orders (product_id, customer_name, quantity, total_price) VALUES (%s, %s, %s, %s)",
                    (product_id, customer_name, quantity, total_price)
                )
                order_count += 1
            except Error:
                pass
        
        connection.commit()
        print(f"  ✅ {order_count} sample orders created")
        
        # 6. Summary
        print("\n" + "=" * 60)
        print("Database Loaded Successfully!")
        print("=" * 60)
        print(f"\n✅ Categories: {len(categories_data)}")
        print(f"✅ Products: {product_count}")
        print(f"✅ Sample Orders: {order_count}")
        print(f"\n🛒 Supermarket inventory ready!")
        print(f"\n📊 You can now login with:")
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print(f"\n🚀 Run: python main.py")
        print()
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"\n❌ Database Error: {e}")
        print("\nPlease make sure:")
        print("  1. MySQL server is running")
        print("  2. Database exists (run setup_database.bat)")
        print("  3. Correct credentials in config.py")
        return False
    
    return True

if __name__ == "__main__":
    load_supermarket_data()
    input("\nPress Enter to exit...")

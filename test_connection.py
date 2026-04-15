"""
MySQL Connection Diagnostic Tool
Helps troubleshoot MySQL connection issues
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

print("=" * 60)
print("MySQL Connection Diagnostic Tool")
print("=" * 60)

# Display current config
print("\n📋 Current Configuration:")
print(f"  Host: {DB_CONFIG['host']}")
print(f"  Port: {DB_CONFIG['port']}")
print(f"  User: {DB_CONFIG['user']}")
print(f"  Database: {DB_CONFIG['database']}")

# Test connection
print("\n🔍 Testing Connection...")
try:
    connection = mysql.connector.connect(**DB_CONFIG)
    if connection.is_connected():
        print("✅ Successfully connected to MySQL!")
        
        # Get MySQL version
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ MySQL Version: {version[0]}")
        
        # Check if database exists
        cursor.execute("SHOW DATABASES LIKE 'smart_management_system'")
        if cursor.fetchone():
            print("✅ Database 'smart_management_system' exists")
        else:
            print("❌ Database 'smart_management_system' NOT found")
            print("   Please run: sql/schema.sql")
        
        cursor.close()
        connection.close()
except Error as e:
    print(f"❌ Connection Failed: {e}")
    print("\n🔧 Troubleshooting Steps:")
    print("   1. Make sure MySQL Server is running")
    print("   2. Check your credentials in config.py")
    print("   3. Verify MySQL is listening on localhost:3306")
    print("   4. Check firewall settings")

print("\n" + "=" * 60)
print("Instructions to Start MySQL:")
print("=" * 60)
print("\nOn Windows with MySQL installed:")
print("  Option 1: Use Services")
print("    - Press Win+R, type 'services.msc'")
print("    - Find 'MySQL' or 'MySQL80' (version may vary)")
print("    - Right-click and select 'Start'")
print("\n  Option 2: Command Line (as Administrator)")
print("    - net start MySQL80")
print("    (or 'MySQL57', 'MySQL' depending on your version)")
print("\n  Option 3: MySQL Workbench")
print("    - Open MySQL Workbench")
print("    - Connections should show MySQL server status")
print("\n" + "=" * 60)

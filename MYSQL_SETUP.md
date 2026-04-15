# MySQL Setup & Troubleshooting Guide

## 🔴 Current Issue
MySQL Server is NOT running on your system. The application cannot connect to the database.

---

## ✅ Step 1: Verify MySQL is Installed
Your system has MySQL 5.5 installed. If you want to upgrade, download the latest version from https://www.mysql.com/downloads/

---

## 🚀 Step 2: Start MySQL Service

### **OPTION A: Using Services (GUI)**
1. Right-click on the Windows Start button
2. Select "Run" (or press Win+R)
3. Type: `services.msc`
4. Press Enter
5. In the Services window, look for any of these:
   - "MySQL"
   - "MySQL55"
   - "MySQL80"
   - "MySQLxx" (any version)
6. If you find it:
   - Right-click → "Start"
   - Wait for Status to show "Running"

### **OPTION B: Using Command Prompt (Recommended)**
1. Right-click on Command Prompt
2. Select "Run as Administrator" (IMPORTANT!)
3. Try these commands one by one:
   ```
   net start MySQL55
   ```
   or
   ```
   net start MySQL
   ```
   or check service name:
   ```
   sc query | findstr MySQL
   ```

### **OPTION C: Using MySQL Command Line**
1. Open Command Prompt as Administrator
2. Navigate to MySQL bin folder:
   ```
   cd "C:\Program Files\MySQL\MySQL Server 5.5\bin"
   ```
3. Try:
   ```
   mysqld --install
   net start MySQL
   ```

---

## 🔍 Step 3: Verify MySQL is Running
Open Command Prompt and type:
```
mysql -u root -p
```
- Press Enter when asked for password (if no password set)
- You should see: `mysql>`
- Type `exit` to quit

---

## 📦 Step 4: Create Database & Tables
1. Open Command Prompt as Administrator
2. Navigate to your project:
   ```
   cd C:\Users\msi\Desktop\tkinter\Projet-tkinter
   ```
3. Connect to MySQL:
   ```
   mysql -u root -p < sql/schema.sql
   ```
   - Press Enter when asked for password
   - Wait for it to complete

---

## 🔐 Step 5: Set MySQL Password (Optional but Recommended)
If you want to set a password:
```
mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_password';
FLUSH PRIVILEGES;
```

Then update your `config.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # Your new password
    'database': 'smart_management_system',
    'port': 3306
}
```

---

## 🧪 Step 6: Test the Connection
Run this test script:
```
python test_connection.py
```

You should see:
```
✅ Successfully connected to MySQL!
✅ MySQL Version: 5.5.16
✅ Database 'smart_management_system' exists
```

---

## 🎯 Step 7: Run Your Application
Once MySQL is running and database is created:
```
python main.py
```

---

## ❌ If You Still Get Errors

### **Error: "Can't connect to MySQL server"**
- MySQL is not running - start it using options above
- Check firewall is not blocking port 3306
- Verify credentials in config.py

### **Error: "Unknown database"**
- Run `sql/schema.sql` to create database and tables
- Check you used the correct database name

### **Error: "Access denied"**
- Check username and password in config.py
- Verify user has permissions

---

## 💡 Troubleshooting Commands

### **Check if MySQL Service Exists:**
```
sc query MySQL
```

### **List all MySQL-related Services:**
```
wmic service list | findstr MySQL
```

### **Check MySQL Port:**
```
netstat -an | findstr 3306
```

### **View MySQL Error Log:**
```
cd "C:\Program Files\MySQL\MySQL Server 5.5\data"
notepad *.err
```

---

## 📞 Need More Help?

If none of the above works:
1. Download and install MySQL Community Server from https://dev.mysql.com/downloads/mysql/
2. Use MySQL Installer which automatically sets up the service
3. Choose "MySQL as a Windows Service" option during installation
4. Start the service using Services.msc

---

## ✨ Quick Reference

| Task | Command |
|------|---------|
| Start MySQL | `net start MySQL55` (as Admin) |
| Stop MySQL | `net stop MySQL55` (as Admin) |
| Login to MySQL | `mysql -u root -p` |
| Create Database | `mysql -u root < sql/schema.sql` |
| Test Connection | `python test_connection.py` |
| Run App | `python main.py` |

# 📦 Inventory Intelligence Platform

A modern, production-ready **Inventory Management System** built with **Flask**, designed to help businesses manage products, suppliers, categories, and stock levels through an intuitive dashboard and role-based access control system.





---

## ✨ Features

### 🔐 Authentication & Authorization

* Secure user authentication
* Google OAuth login support
* Role-Based Access Control (RBAC)
* Session management
* Password hashing

### 📦 Inventory Management

* Add, edit, and delete products
* SKU management
* Inventory valuation
* Product descriptions and categorization
* Real-time stock updates

### 🏷️ Category Management

* Create and manage categories
* Category-wise inventory analytics
* Product grouping

### 🚚 Supplier Management

* Supplier profiles
* Contact information management
* Supplier-product relationships

### 📊 Dashboard & Analytics

* Inventory health score
* Low-stock monitoring
* Category analytics
* Interactive charts using Chart.js
* AI-powered stock recommendations

### 🔔 Notification System

* Real-time notifications
* Low-stock alerts
* System activity tracking
* Notification history

---

# 🖼️ Application Preview

### Dashboard

* Inventory Health Score
* AI Recommendations
* Stock Monitoring
* Analytics Charts

### Inventory Module

* Product Cards & Table View
* Search & Filtering
* Stock Updates
* Supplier Information

---

# 🏗️ Project Architecture

```text
Inventory Intelligence Platform
│
├── Authentication System
├── Dashboard & Analytics
├── Inventory Management
├── Category Management
├── Supplier Management
├── Notification System
└── Role-Based Access Control
```

---

# 🛠️ Tech Stack

## Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-Login
* Flask-WTF
* Flask-SocketIO
* Authlib

## Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Chart.js
* Lucide Icons

## Database

* SQLite

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/inventory-intelligence-platform.git
cd inventory-intelligence-platform
```

## Create Virtual Environment

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Apply Database Migrations

```bash
flask db upgrade
```

---

## Run Application

```bash
python run.py
```

Application will start at:

```text
http://127.0.0.1:5000
```

---

# 🔑 Demo Credentials

| Field    | Value                                         |
| -------- | --------------------------------------------- |
| Username | demo                           |
| Email    | [demo@inventory.com](mailto:demo@inventory.com) |
| Password | Demo@123                                    |

---

# 👥 User Roles

## Admin

* Manage users
* Manage inventory
* Manage suppliers
* Manage categories
* Access analytics dashboard

## Manager

* Manage inventory
* Manage suppliers
* Manage categories
* Access analytics

## Employee

* View inventory
* Update stock quantities

---

# 📁 Database

SQLite database location:

```text
instance/inventory_intelligence.sqlite
```

The application automatically:

* Creates default roles
* Seeds the admin account
* Verifies seed data during startup

---

# 🔮 Future Enhancements

* Sales & Billing System
* Purchase Orders
* Barcode Scanning
* Demand Forecasting using Machine Learning
* Email Notifications
* Multi-Warehouse Support
* Export Reports (PDF/Excel)
* Cloud Deployment

---

# 🤝 Contributing

Contributions, issues, and feature requests are welcome.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**MD Gulam Mustafa**

* GitHub: https://github.com/Gulammustafa03

---

⭐ If you like this project, consider giving it a star on GitHub.

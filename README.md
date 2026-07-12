# MostOdd Marketplace

## Overview

MostOdd Marketplace is a Django-based eCommerce web application that allows Vendors to create and manage online stores while Buyers can browse products, purchase items, and leave verified reviews.

The application demonstrates user authentication, role-based access control, shopping cart functionality, order processing, inventory management, email notifications, and the Django admin interface.

---

## Features

### Authentication

- User Registration
- User Login
- User Logout
- Password Reset via Email
- Role-based access (Buyer and Vendor)

### Vendor Features

- Create Store
- Edit Store
- Delete Store
- Create Products
- Edit Products
- Delete Products
- Vendor Dashboard
- Manage personal stores and products only

### Buyer Features

- Browse Products
- Browse Stores
- Add Products to Cart
- Update Cart Quantity
- Remove Products from Cart
- Checkout
- Receive Order Confirmation Email
- Leave Product Reviews
- Verified Purchase Reviews

### Shopping Cart

- Session-based cart
- Increase quantity
- Decrease quantity
- Remove products
- Automatic total calculation
- Stock validation

### Order Management

- Order creation
- Order items
- Order history
- Automatic stock updates
- Invoice generation

### Admin Panel

The Django admin allows administrators to manage:

- Users
- Stores
- Products
- Orders
- Order Items
- Reviews

Searching and filtering have been configured for easier management.

---

## Technologies Used

- Python 3
- Django
- SQLite
- HTML5
- Bootstrap 5
- CSS

---

## Installation

### Clone the repository

```bash
git clone <repository-url>
```

### Navigate into the project

```bash
cd Django-Ecommerce
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply migrations

```bash
python manage.py migrate
```

### Create a superuser

```bash
python manage.py createsuperuser
```

### Run the development server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## User Roles

### Buyer

- Browse products
- Purchase products
- Manage shopping cart
- Leave reviews

### Vendor

- Create stores
- Manage products
- View Vendor Dashboard

---

## Security Features

- Login required for protected pages
- Role-based permissions
- Vendor ownership validation
- Password reset
- Stock validation during checkout

---

## Project Structure

```
store/
│
├── migrations/
├── templates/
├── static/
├── admin.py
├── forms.py
├── models.py
├── urls.py
├── views.py
```

---

## Future Improvements

- Product images
- Product categories
- Search functionality
- Wishlist
- Payment gateway integration
- Order tracking
- Sales analytics
- Product sorting and filtering

---

## Author

Phumelela Mdingi

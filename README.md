# MakeUp Store Django Project

A comprehensive Django-based e-commerce platform for makeup products with user authentication, product management, and promotional features.

## Features

### Product Management
- Product listing with advanced filtering options
- Category-based product organization
- Product search functionality
- Pagination system (5 products per page)
- Product details view
- Add new products (with permission control)

### User Authentication System
- Custom user registration with email confirmation
- Custom login with "Remember Me" functionality
- User profile management
- Password change functionality
- Session management
- Permission-based access control

### Contact System
- Contact form with JSON storage
- Message filtering by type and name
- Age calculation from birth date
- Message preprocessing and storage
- Message listing interface

### Promotion System
- Create and manage promotional campaigns
- Category-based promotions
- Automated email notifications for eligible users
- User engagement tracking through product views
- Promotion expiration management

### Error Handling
- Custom 403 (Forbidden) error pages
- Personalized error messages
- User-specific error handling

## Technical Implementation

### Forms
- Custom user creation form
- Product filter form
- Contact form
- Authentication form
- Promotion form

### Database Models
- Product model with category and brand relationships
- Custom user model
- Category model
- Promotion model
- View tracking model

### Additional Features
- Email templating system
- JSON-based message storage
- Prefetch-related and select-related optimizations
- Django permissions integration
- Session management
- Mass email capabilities

## Installation

1. Clone the repository
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Apply database migrations:
```
python manage.py migrate
```
4. Create a superuser:
```
python manage.py createsuperuser
```
5. Run the development server:
```
python manage.py runserver
```

## Usage

Access the application at `http://127.0.0.1:8000/` and use the following endpoints:

- `/proiect/lista_produse/` - View all products
- `/proiect/filtreaza_produse/` - Filter products
- `/proiect/contact/` - Contact form
- `/proiect/register/` - User registration
- `/proiect/login/` - User login
- `/proiect/profile/` - User profile

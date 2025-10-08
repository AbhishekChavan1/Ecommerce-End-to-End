"""
Application entry point.
This module provides the Flask application instance for running the server.

Usage:
    Development: flask run
    Production: gunicorn -w 4 -b 0.0.0.0:8000 run:app
"""

import os
from app import create_app, db
from app.models import User, Product, Category, Cart, CartItem, Order, OrderItem

# Create application instance
app = create_app(os.getenv('FLASK_ENV') or 'development')


@app.shell_context_processor
def make_shell_context():
    """
    Make database models available in Flask shell.
    Usage: flask shell
    """
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'Category': Category,
        'Cart': Cart,
        'CartItem': CartItem,
        'Order': Order,
        'OrderItem': OrderItem
    }


@app.cli.command()
def init_db():
    """Initialize the database with tables and sample data."""
    db.create_all()
    
    # Create categories
    categories = [
        Category(name='Electronics', description='Electronic devices and gadgets'),
        Category(name='Clothing', description='Fashion and apparel'),
        Category(name='Books', description='Books and educational materials'),
        Category(name='Home & Garden', description='Home improvement and gardening'),
        Category(name='Sports', description='Sports and fitness equipment')
    ]
    
    for category in categories:
        db.session.add(category)
    
    # Create admin user
    admin_email = app.config['ADMIN_EMAIL']
    admin_password = app.config['ADMIN_PASSWORD']
    
    admin_user = User(
        username='admin',
        email=admin_email,
        first_name='Admin',
        last_name='User',
        is_admin=True
    )
    admin_user.set_password(admin_password)
    db.session.add(admin_user)
    
    # Create sample products
    sample_products = [
        Product(
            name='Laptop Computer',
            description='High-performance laptop for work and gaming',
            price=999.99,
            category_id=1,
            stock_quantity=10,
            image_filename='laptop.jpg'
        ),
        Product(
            name='Smartphone',
            description='Latest model smartphone with advanced features',
            price=699.99,
            category_id=1,
            stock_quantity=15,
            image_filename='smartphone.jpg'
        ),
        Product(
            name='T-Shirt',
            description='Comfortable cotton t-shirt',
            price=19.99,
            category_id=2,
            stock_quantity=50,
            image_filename='tshirt.jpg'
        )
    ]
    
    for product in sample_products:
        db.session.add(product)
    
    db.session.commit()
    print('Database initialized with sample data!')


@app.cli.command()
def create_admin():
    """Create an admin user."""
    from app.models.user import User
    
    admin_email = input('Admin email: ')
    admin_password = input('Admin password: ')
    
    admin_user = User(
        username='admin',
        email=admin_email,
        first_name='Admin',
        last_name='User',
        is_admin=True
    )
    admin_user.set_password(admin_password)
    
    db.session.add(admin_user)
    db.session.commit()
    print(f'Admin user created: {admin_email}')


if __name__ == '__main__':
    app.run(debug=True)
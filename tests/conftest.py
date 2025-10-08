"""
Unit Tests Configuration and Fixtures.
Provides test configuration and shared fixtures for unit testing.

Quality Management Principles:
- Test Isolation: Each test runs in isolated environment
- Data Integrity: Consistent test data setup and teardown
- Coverage: Comprehensive test coverage for all components
- Maintainability: Reusable fixtures and utilities
"""

import pytest
import tempfile
import os
from app import create_app, db
from app.models import User, Product, Category, Cart, CartItem, Order, OrderItem
from config.config import TestingConfig


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    # Create temporary database
    db_fd, db_path = tempfile.mkstemp()
    
    # Override database configuration
    test_config = TestingConfig()
    test_config.SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    test_config.WTF_CSRF_ENABLED = False
    
    app = create_app('testing')
    app.config.from_object(test_config)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    
    # Clean up temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def auth_headers():
    """Create authentication headers for API tests."""
    return {'Content-Type': 'application/json'}


# Database Fixtures
@pytest.fixture
def clean_db(app):
    """Clean database before each test."""
    with app.app_context():
        # Clear all tables
        db.session.query(OrderItem).delete()
        db.session.query(Order).delete()
        db.session.query(CartItem).delete()
        db.session.query(Cart).delete()
        db.session.query(Product).delete()
        db.session.query(Category).delete()
        db.session.query(User).delete()
        db.session.commit()
        yield db
        # Clean up after test
        db.session.rollback()


# User Fixtures
@pytest.fixture
def sample_user(clean_db):
    """Create a sample user for testing."""
    user = User(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User',
        phone='555-0123',
        address_line1='123 Test St',
        city='Test City',
        state='TS',
        postal_code='12345',
        country='Test Country'
    )
    user.set_password('TestPassword123')
    clean_db.session.add(user)
    clean_db.session.commit()
    return user


@pytest.fixture
def admin_user(clean_db):
    """Create an admin user for testing."""
    admin = User(
        username='admin',
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        is_admin=True
    )
    admin.set_password('AdminPassword123')
    clean_db.session.add(admin)
    clean_db.session.commit()
    return admin


# Category Fixtures
@pytest.fixture
def sample_category(clean_db):
    """Create a sample category for testing."""
    category = Category(
        name='Electronics',
        description='Electronic devices and gadgets'
    )
    clean_db.session.add(category)
    clean_db.session.commit()
    return category


@pytest.fixture
def multiple_categories(clean_db):
    """Create multiple categories for testing."""
    categories = [
        Category(name='Electronics', description='Electronic devices'),
        Category(name='Clothing', description='Fashion and apparel'),
        Category(name='Books', description='Books and educational materials'),
    ]
    for category in categories:
        clean_db.session.add(category)
    clean_db.session.commit()
    return categories


# Product Fixtures
@pytest.fixture
def sample_product(clean_db, sample_category):
    """Create a sample product for testing."""
    product = Product(
        name='Test Laptop',
        description='A test laptop for testing',
        price=999.99,
        category_id=sample_category.id,
        stock_quantity=10,
        sku='TEST-LAPTOP-001'
    )
    clean_db.session.add(product)
    clean_db.session.commit()
    return product


@pytest.fixture
def multiple_products(clean_db, sample_category):
    """Create multiple products for testing."""
    products = [
        Product(
            name='Laptop',
            description='High-performance laptop',
            price=999.99,
            category_id=sample_category.id,
            stock_quantity=5,
            is_featured=True
        ),
        Product(
            name='Mouse',
            description='Wireless mouse',
            price=29.99,
            category_id=sample_category.id,
            stock_quantity=20
        ),
        Product(
            name='Keyboard',
            description='Mechanical keyboard',
            price=149.99,
            category_id=sample_category.id,
            stock_quantity=0  # Out of stock
        ),
    ]
    for product in products:
        clean_db.session.add(product)
    clean_db.session.commit()
    return products


@pytest.fixture
def sale_product(clean_db, sample_category):
    """Create a product on sale for testing."""
    product = Product(
        name='Sale Item',
        description='Product on sale',
        price=100.00,
        sale_price=79.99,
        category_id=sample_category.id,
        stock_quantity=5
    )
    clean_db.session.add(product)
    clean_db.session.commit()
    return product


# Cart Fixtures
@pytest.fixture
def sample_cart(clean_db, sample_user):
    """Create a sample cart for testing."""
    cart = Cart(user_id=sample_user.id)
    clean_db.session.add(cart)
    clean_db.session.commit()
    return cart


@pytest.fixture
def cart_with_items(clean_db, sample_cart, multiple_products):
    """Create a cart with items for testing."""
    # Add items to cart
    for i, product in enumerate(multiple_products[:2]):  # Add first 2 products
        cart_item = CartItem(
            cart_id=sample_cart.id,
            product_id=product.id,
            quantity=i + 1,
            price=product.get_effective_price()
        )
        clean_db.session.add(cart_item)
    clean_db.session.commit()
    return sample_cart


# Order Fixtures
@pytest.fixture
def sample_shipping_address():
    """Create sample shipping address for testing."""
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '555-0123',
        'address_line1': '123 Main St',
        'address_line2': 'Apt 4B',
        'city': 'Anytown',
        'state': 'ST',
        'postal_code': '12345',
        'country': 'United States'
    }


@pytest.fixture
def sample_order(clean_db, sample_user, sample_shipping_address, multiple_products):
    """Create a sample order for testing."""
    order = Order(
        user_id=sample_user.id,
        shipping_address=sample_shipping_address,
        payment_method='credit_card'
    )
    clean_db.session.add(order)
    clean_db.session.flush()  # Get order ID
    
    # Add order items
    for product in multiple_products[:2]:
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=1,
            price=product.get_effective_price()
        )
        clean_db.session.add(order_item)
    
    # Calculate totals
    order.calculate_totals()
    clean_db.session.commit()
    return order


# Authentication Fixtures
@pytest.fixture
def logged_in_user(client, sample_user):
    """Log in a user and return the client."""
    client.post('/auth/login', data={
        'username_or_email': sample_user.username,
        'password': 'TestPassword123'
    })
    return client


@pytest.fixture
def logged_in_admin(client, admin_user):
    """Log in an admin user and return the client."""
    client.post('/auth/login', data={
        'username_or_email': admin_user.username,
        'password': 'AdminPassword123'
    })
    return client


# Selenium Test Fixtures
@pytest.fixture
def test_user_data():
    """Provide test user data for Selenium tests."""
    def _create_user_data(username=None):
        import random
        import string
        
        if username is None:
            username = 'testuser' + ''.join(random.choices(string.digits, k=4))
        
        return {
            'first_name': 'Test',
            'last_name': 'User',
            'username': username,
            'email': f'{username}@example.com',
            'password': 'TestPassword123'
        }
    return _create_user_data


@pytest.fixture
def sample_products():
    """Provide sample products for Selenium tests."""
    return [
        {
            'name': 'Test Laptop',
            'price': 999.99,
            'description': 'High-performance laptop for testing'
        },
        {
            'name': 'Test Mouse',
            'price': 29.99,
            'description': 'Wireless mouse for testing'
        },
        {
            'name': 'Test Keyboard',
            'price': 149.99,
            'description': 'Mechanical keyboard for testing'
        }
    ]


@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    """Set up initial test data for Selenium tests."""
    # This would typically create initial data in the test database
    # For now, we'll rely on the application's initialization
    pass


# Test Data Factories
class UserFactory:
    """Factory for creating test users."""
    
    @staticmethod
    def create(username='testuser', email='test@example.com', **kwargs):
        """Create a user with default or custom attributes."""
        defaults = {
            'first_name': 'Test',
            'last_name': 'User',
            'is_admin': False
        }
        defaults.update(kwargs)
        
        user = User(username=username, email=email, **defaults)
        user.set_password('TestPassword123')
        return user


class ProductFactory:
    """Factory for creating test products."""
    
    @staticmethod
    def create(name='Test Product', category_id=1, **kwargs):
        """Create a product with default or custom attributes."""
        defaults = {
            'description': 'A test product',
            'price': 99.99,
            'stock_quantity': 10
        }
        defaults.update(kwargs)
        
        return Product(name=name, category_id=category_id, **defaults)


class CategoryFactory:
    """Factory for creating test categories."""
    
    @staticmethod
    def create(name='Test Category', **kwargs):
        """Create a category with default or custom attributes."""
        defaults = {
            'description': 'A test category'
        }
        defaults.update(kwargs)
        
        return Category(name=name, **defaults)
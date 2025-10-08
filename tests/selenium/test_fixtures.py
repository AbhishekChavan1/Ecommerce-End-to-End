"""
Test fixtures and configuration for Selenium tests.
Provides test data, user management, and database setup for comprehensive testing.
"""

import pytest
import sys
import os
from datetime import datetime

# Add the app directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app import create_app, db
from app.models import User, Product, Category, Cart, CartItem, Order, OrderItem
from werkzeug.security import generate_password_hash


@pytest.fixture(scope='session')
def app():
    """Create application instance for testing."""
    app = create_app('testing')
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create test data
        setup_test_data()
        
        yield app
        
        # Cleanup
        db.drop_all()


@pytest.fixture(scope='session')
def app_context(app):
    """Create application context for testing."""
    with app.app_context():
        yield app


def setup_test_data():
    """Set up test data for comprehensive testing."""
    
    # Create test categories
    categories = [
        Category(name='Electronics', description='Electronic items and gadgets'),
        Category(name='Clothing', description='Fashion and apparel'),
        Category(name='Books', description='Books and literature'),
        Category(name='Home & Garden', description='Home and garden items'),
        Category(name='Sports', description='Sports and fitness equipment')
    ]
    
    for category in categories:
        db.session.add(category)
    
    db.session.commit()
    
    # Create test products
    products = [
        Product(
            name='Premium Laptop',
            description='High-performance laptop for professionals',
            price=1299.99,
            category_id=1,
            image_filename='laptop.jpg',
            stock_quantity=10
        ),
        Product(
            name='Smartphone Pro',
            description='Latest smartphone with advanced features',
            price=899.99,
            category_id=1,
            image_filename='phone.jpg',
            stock_quantity=15
        ),
        Product(
            name='Wireless Headphones',
            description='Premium noise-cancelling wireless headphones',
            price=199.99,
            category_id=1,
            image_filename='headphones.jpg',
            stock_quantity=25
        ),
        Product(
            name='Designer T-Shirt',
            description='Comfortable cotton t-shirt with modern design',
            price=29.99,
            category_id=2,
            image_filename='tshirt.jpg',
            stock_quantity=50
        ),
        Product(
            name='Classic Jeans',
            description='Durable denim jeans with perfect fit',
            price=79.99,
            category_id=2,
            image_filename='jeans.jpg',
            stock_quantity=30
        ),
        Product(
            name='Programming Guide',
            description='Comprehensive guide to modern programming',
            price=49.99,
            category_id=3,
            image_filename='book.jpg',
            stock_quantity=20
        ),
        Product(
            name='Fiction Novel',
            description='Bestselling fiction novel',
            price=19.99,
            category_id=3,
            image_filename='novel.jpg',
            stock_quantity=40
        ),
        Product(
            name='Garden Tool Set',
            description='Complete set of essential garden tools',
            price=89.99,
            category_id=4,
            image_filename='tools.jpg',
            stock_quantity=12
        ),
        Product(
            name='Yoga Mat',
            description='Non-slip yoga mat for comfortable practice',
            price=39.99,
            category_id=5,
            image_filename='yoga.jpg',
            stock_quantity=35
        ),
        Product(
            name='Running Shoes',
            description='Lightweight running shoes with excellent support',
            price=129.99,
            category_id=5,
            image_filename='shoes.jpg',
            stock_quantity=18
        )
    ]
    
    for product in products:
        db.session.add(product)
    
    db.session.commit()
    
    # Create test users
    test_users = [
        User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password_hash=generate_password_hash('testpass123')
        ),
        User(
            username='johnsmith',
            email='john@example.com',
            first_name='John',
            last_name='Smith',
            password_hash=generate_password_hash('password123')
        ),
        User(
            username='janedoe',
            email='jane@example.com',
            first_name='Jane',
            last_name='Doe',
            password_hash=generate_password_hash('securepass')
        ),
        User(
            username='admin',
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password_hash=generate_password_hash('adminpass'),
            is_admin=True
        )
    ]
    
    for user in test_users:
        db.session.add(user)
    
    db.session.commit()


class TestData:
    """Test data constants and helper methods."""
    
    # Test users
    VALID_USER = {
        'username': 'testuser',
        'password': 'testpass123',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    ADMIN_USER = {
        'username': 'admin',
        'password': 'adminpass',
        'email': 'admin@example.com',
        'first_name': 'Admin',
        'last_name': 'User'
    }
    
    NEW_USER = {
        'username': 'newuser',
        'password': 'newpass123',
        'email': 'newuser@example.com',
        'first_name': 'New',
        'last_name': 'User'
    }
    
    # Invalid user data for negative testing
    INVALID_USERS = [
        {
            'username': '',
            'password': 'pass123',
            'email': 'invalid@example.com',
            'error': 'Username required'
        },
        {
            'username': 'testinvalid',
            'password': '',
            'email': 'invalid@example.com',
            'error': 'Password required'
        },
        {
            'username': 'testinvalid',
            'password': '123',
            'email': 'invalid@example.com',
            'error': 'Password too short'
        },
        {
            'username': 'testuser',  # Existing username
            'password': 'pass123',
            'email': 'duplicate@example.com',
            'error': 'Username already exists'
        },
        {
            'username': 'testnew',
            'password': 'pass123',
            'email': 'invalid-email',
            'error': 'Invalid email format'
        }
    ]
    
    # Shipping information for checkout
    SHIPPING_INFO = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '+1-555-123-4567',
        'address': '123 Main Street',
        'address2': 'Apt 4B',
        'city': 'New York',
        'state': 'NY',
        'postal_code': '10001',
        'country': 'United States'
    }
    
    # Product search terms
    SEARCH_TERMS = [
        {'term': 'laptop', 'should_find': True, 'expected_count': 1},
        {'term': 'shirt', 'should_find': True, 'expected_count': 1},
        {'term': 'book', 'should_find': True, 'expected_count': 2},
        {'term': 'nonexistent', 'should_find': False, 'expected_count': 0},
        {'term': '', 'should_find': True, 'expected_count': 10}  # All products
    ]
    
    # Category filters
    CATEGORIES = [
        {'name': 'Electronics', 'expected_count': 3},
        {'name': 'Clothing', 'expected_count': 2},
        {'name': 'Books', 'expected_count': 2},
        {'name': 'Home & Garden', 'expected_count': 1},
        {'name': 'Sports', 'expected_count': 2}
    ]
    
    # Sort options
    SORT_OPTIONS = [
        {'value': 'name_asc', 'name': 'Name (A-Z)'},
        {'value': 'name_desc', 'name': 'Name (Z-A)'},
        {'value': 'price_asc', 'name': 'Price (Low to High)'},
        {'value': 'price_desc', 'name': 'Price (High to Low)'}
    ]
    
    # Cart test scenarios
    CART_SCENARIOS = [
        {'product_index': 0, 'quantity': 1, 'expected_name': 'Premium Laptop'},
        {'product_index': 1, 'quantity': 2, 'expected_name': 'Smartphone Pro'},
        {'product_index': 3, 'quantity': 3, 'expected_name': 'Designer T-Shirt'}
    ]
    
    # Payment methods
    PAYMENT_METHODS = [
        'credit_card',
        'debit_card',
        'paypal',
        'bank_transfer'
    ]
    
    @staticmethod
    def get_product_by_name(name):
        """Get product by name for testing."""
        with db.session() as session:
            return session.query(Product).filter_by(name=name).first()
    
    @staticmethod
    def get_user_by_username(username):
        """Get user by username for testing."""
        with db.session() as session:
            return session.query(User).filter_by(username=username).first()
    
    @staticmethod
    def cleanup_test_user(username):
        """Clean up test user after testing."""
        with db.session() as session:
            user = session.query(User).filter_by(username=username).first()
            if user:
                session.delete(user)
                session.commit()
    
    @staticmethod
    def create_cart_with_items(user_id, product_quantities):
        """Create cart with specific items for testing."""
        with db.session() as session:
            cart = Cart(user_id=user_id)
            session.add(cart)
            session.commit()
            
            for product_id, quantity in product_quantities.items():
                cart_item = CartItem(
                    cart_id=cart.id,
                    product_id=product_id,
                    quantity=quantity
                )
                session.add(cart_item)
            
            session.commit()
            return cart.id


class TestConfig:
    """Test configuration constants."""
    
    # Base URL for testing
    BASE_URL = "http://localhost:5000"
    
    # Timeouts
    DEFAULT_TIMEOUT = 10
    LONG_TIMEOUT = 30
    SHORT_TIMEOUT = 5
    
    # Browser settings
    WINDOW_SIZE = (1920, 1080)
    HEADLESS = False  # Set to True for CI/CD
    
    # Test user credentials
    TEST_USERNAME = "testuser"
    TEST_PASSWORD = "testpass123"
    
    # Screenshots directory
    SCREENSHOT_DIR = "tests/selenium/screenshots"
    
    # Test data directory
    TEST_DATA_DIR = "tests/selenium/test_data"
    
    @staticmethod
    def create_directories():
        """Create necessary test directories."""
        os.makedirs(TestConfig.SCREENSHOT_DIR, exist_ok=True)
        os.makedirs(TestConfig.TEST_DATA_DIR, exist_ok=True)


class TestUtils:
    """Utility functions for testing."""
    
    @staticmethod
    def generate_unique_username():
        """Generate unique username for testing."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"testuser_{timestamp}"
    
    @staticmethod
    def generate_unique_email():
        """Generate unique email for testing."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"test_{timestamp}@example.com"
    
    @staticmethod
    def wait_for_element_text(driver, locator, expected_text, timeout=10):
        """Wait for element to contain expected text."""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.text_to_be_present_in_element(locator, expected_text))
    
    @staticmethod
    def take_screenshot(driver, filename):
        """Take screenshot for debugging."""
        TestConfig.create_directories()
        filepath = os.path.join(TestConfig.SCREENSHOT_DIR, filename)
        driver.save_screenshot(filepath)
        return filepath
    
    @staticmethod
    def verify_url_contains(driver, expected_url_part):
        """Verify current URL contains expected part."""
        current_url = driver.current_url
        return expected_url_part in current_url
    
    @staticmethod
    def get_element_text_safe(driver, locator):
        """Safely get element text, return empty string if not found."""
        try:
            element = driver.find_element(*locator)
            return element.text
        except Exception:
            return ""
# E-commerce Selenium Testing Framework

## Overview

This is a comprehensive, object-oriented Selenium testing framework for the E-commerce Flask application. The framework implements the **Page Object Model (POM)** design pattern and follows industry best practices for maintainable, scalable test automation.

## 🏗️ Architecture

### Page Object Model Structure

```
tests/selenium/
├── base.py                 # Base classes for Selenium tests
├── pages/
│   ├── __init__.py        # Page objects package
│   └── page_objects.py    # All page object classes
├── test_fixtures.py       # Test data and fixtures
├── test_ecommerce_ui.py   # Main test suite
├── test_runner.py         # Advanced test runner
├── run_tests.py           # Simple test runner
└── reports/               # Test reports and screenshots
```

### Key Components

1. **Base Classes** (`base.py`)
   - `BaseSeleniumTest`: Common test setup and teardown
   - `BasePage`: Common page interactions and utilities

2. **Page Objects** (`pages/page_objects.py`)
   - `HomePage`: Home page interactions
   - `LoginPage`: Authentication functionality
   - `RegisterPage`: User registration
   - `ProductListPage`: Product browsing and search
   - `ProductDetailPage`: Product details and add-to-cart
   - `CartPage`: Shopping cart management
   - `CheckoutPage`: Order completion
   - `OrderConfirmationPage`: Order confirmation

3. **Test Fixtures** (`test_fixtures.py`)
   - Test data management
   - Database setup and teardown
   - User and product fixtures

## 🚀 Features

### Comprehensive Test Coverage

- ✅ User authentication (login/registration)
- ✅ Product browsing and search
- ✅ Shopping cart operations
- ✅ Checkout process with dummy payment
- ✅ Responsive design testing
- ✅ Error handling and validation
- ✅ AJAX functionality testing

### Quality Management

- **Test Independence**: Each test can run in isolation
- **Data Management**: Structured test data with fixtures
- **Error Handling**: Graceful failure with informative messages
- **Screenshot Capture**: Automatic screenshots on test failures
- **Reporting**: HTML test reports with detailed information

### Cross-browser Support

- Chrome (default)
- Firefox (configurable)
- Headless mode support
- Mobile viewport testing

## 📋 Prerequisites

### Software Requirements

- Python 3.8+
- Google Chrome or Firefox
- ChromeDriver or GeckoDriver

### Python Dependencies

```bash
pip install selenium
pip install pytest
pip install pytest-html
pip install webdriver-manager
pip install requests
```

## 🏃‍♂️ Running Tests

### Quick Start

1. **Start the Flask application:**

   ```bash
   python run.py
   ```

2. **Run demonstration tests:**

   ```bash
   python demo_tests.py
   ```

### Advanced Test Execution

#### Run All Tests
```bash
python tests/selenium/test_runner.py
```

#### Run Specific Test Groups
```bash
# Authentication tests
python tests/selenium/test_runner.py --test-group auth

# Product browsing tests
python tests/selenium/test_runner.py --test-group products

# Shopping cart tests
python tests/selenium/test_runner.py --test-group cart

# Checkout process tests
python tests/selenium/test_runner.py --test-group checkout
```

#### Headless Mode
```bash
python tests/selenium/test_runner.py --headless
```

#### With Coverage Report
```bash
python tests/selenium/test_runner.py --coverage
```

#### Stop on First Failure
```bash
python tests/selenium/test_runner.py --stop-on-failure
```

### Using pytest Directly
```bash
# Run all Selenium tests
pytest tests/selenium/ -v

# Run specific test class
pytest tests/selenium/test_ecommerce_ui.py::TestUserAuthentication -v

# Run with HTML report
pytest tests/selenium/ --html=reports/test_report.html --self-contained-html
```

## 🧪 Test Structure

### Test Classes
1. **TestUserAuthentication**
   - User registration success/failure
   - User login success/failure
   - Form validation testing

2. **TestProductBrowsing**
   - Home page loading
   - Product search functionality
   - Category filtering
   - Product sorting

3. **TestShoppingCart**
   - Add products to cart
   - Update quantities
   - Remove items
   - Cart calculations

4. **TestCheckoutProcess**
   - Checkout form completion
   - Payment method selection
   - Order confirmation
   - Demo data functionality

5. **TestResponsiveDesign**
   - Mobile viewport testing
   - Element visibility
   - Navigation functionality

6. **TestErrorHandling**
   - Invalid input handling
   - Network error simulation
   - Graceful degradation

### Sample Test Method
```python
def test_add_product_to_cart(self):
    """Test adding a product to cart."""
    # Navigate to products page
    products_page = ProductListPage(self.driver)
    products_page.navigate_to_products()
    
    # Click on first product
    products_page.click_product(0)
    
    # Add to cart
    detail_page = ProductDetailPage(self.driver)
    detail_page.add_to_cart(quantity=2)
    
    # Verify cart count updated
    cart_page = CartPage(self.driver)
    cart_page.navigate_to_cart()
    assert cart_page.get_cart_item_count() == 1
```

## 📊 Test Data Management

### Test Users
- **Valid User**: `testuser` / `testpass123`
- **Admin User**: `admin` / `adminpass`
- **Invalid Users**: Various invalid combinations for negative testing

### Test Products
- Electronics (laptops, phones, headphones)
- Clothing (t-shirts, jeans)
- Books (programming guides, novels)
- Home & Garden items
- Sports equipment

### Shipping Information
Pre-configured shipping data for checkout testing:
```python
SHIPPING_INFO = {
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'john.doe@example.com',
    'phone': '+1-555-123-4567',
    'address': '123 Main Street',
    'city': 'New York',
    'state': 'NY',
    'postal_code': '10001',
    'country': 'United States'
}
```

## 📈 Reporting

### HTML Reports
- Detailed test execution reports
- Screenshots on failures
- Execution time tracking
- Pass/fail statistics

### Console Output
- Real-time test progress
- Detailed error messages
- Test execution summary

### Screenshots
- Automatic capture on test failures
- Stored in `tests/selenium/screenshots/`
- Timestamped for easy identification

## 🔧 Configuration

### Browser Configuration
```python
# Chrome options (in base.py)
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920,1080')

# Headless mode
if os.environ.get('HEADLESS'):
    chrome_options.add_argument('--headless')
```

### Test Configuration
```python
# Base URL for testing
BASE_URL = "http://localhost:5000"

# Timeouts
DEFAULT_TIMEOUT = 10
LONG_TIMEOUT = 30
SHORT_TIMEOUT = 5

# Window size
WINDOW_SIZE = (1920, 1080)
```

## 🔍 Debugging

### Taking Screenshots
```python
# Manual screenshot
TestUtils.take_screenshot(driver, "debug_screenshot.png")

# Automatic on failure
# Screenshots are automatically captured when tests fail
```

### Verbose Output
```bash
# Run with verbose output to see detailed logs
python tests/selenium/test_runner.py --verbose
```

### Debug Mode
```python
# Add breakpoints in test methods
import pdb; pdb.set_trace()
```

## 🚀 Best Practices Implemented

### Page Object Model
- **Encapsulation**: Page-specific logic contained in respective classes
- **Reusability**: Common actions available for test methods
- **Maintainability**: Locators and actions centralized per page

### Test Independence
- Each test can run independently
- No dependencies between test methods
- Clean setup and teardown for each test

### Robust Element Handling
- Explicit waits for element presence
- Error handling for missing elements
- Multiple locator strategies

### Data Management
- Structured test data with fixtures
- Database setup and cleanup
- Unique test data generation

## 📚 Usage Examples

### Basic Page Interaction
```python
# Navigate to login page
login_page = LoginPage(self.driver)
login_page.navigate_to_login()

# Perform login
login_page.login(username="testuser", password="testpass123")

# Verify successful login
assert "login" not in self.driver.current_url
```

### Product Search and Cart
```python
# Search for products
products_page = ProductListPage(self.driver)
products_page.navigate_to_products()
products_page.search_products("laptop")

# Add to cart
products_page.click_product(0)
detail_page = ProductDetailPage(self.driver)
detail_page.add_to_cart(quantity=2)

# Verify cart
cart_page = CartPage(self.driver)
cart_page.navigate_to_cart()
assert cart_page.get_cart_item_count() > 0
```

### Complete Checkout Flow
```python
# Complete checkout process
checkout_page = CheckoutPage(self.driver)
checkout_page.navigate_to_checkout()

# Use demo data
checkout_page.complete_demo_checkout()

# Verify order confirmation
confirmation_page = OrderConfirmationPage(self.driver)
assert confirmation_page.is_success_page_displayed()
```

## 🔧 Maintenance

### Adding New Tests
1. Create test method in appropriate test class
2. Use existing page objects for interactions
3. Follow naming convention: `test_feature_description`
4. Add appropriate assertions

### Adding New Page Objects
1. Create new page class inheriting from `BasePage`
2. Define locators as class attributes
3. Implement page-specific methods
4. Add to `__init__.py` imports

### Updating Locators
1. Update locator definitions in page object classes
2. Test locator changes across all affected tests
3. Update documentation if necessary

## 📋 Troubleshooting

### Common Issues

**Chrome driver issues:**
```bash
# Update ChromeDriver
pip install --upgrade webdriver-manager
```

**Flask app not accessible:**
```bash
# Ensure Flask app is running
python run.py
# Check http://localhost:5000 in browser
```

**Test failures due to timing:**
```python
# Increase timeouts in base.py
DEFAULT_TIMEOUT = 15  # Increase from 10
```

**Database issues:**
```bash
# Reset database
flask db reset
flask db init-db
```

## 🚀 Getting Started

1. **Clone and setup:**
   ```bash
   cd ecommerce_app
   pip install -r requirements.txt
   ```

2. **Initialize database:**
   ```bash
   python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
   ```

3. **Start Flask app:**
   ```bash
   python run.py
   ```

4. **Run tests:**
   ```bash
   python demo_tests.py
   ```

## 📞 Support

For issues or questions about the testing framework:
1. Check the console output for detailed error messages
2. Review the HTML test reports in `tests/selenium/reports/`
3. Check screenshots in `tests/selenium/screenshots/` for visual debugging
4. Verify Flask application is running and accessible

---

**Happy Testing! 🎉**

This comprehensive Selenium testing framework provides robust, maintainable test automation for the E-commerce application using industry best practices and the Page Object Model design pattern.
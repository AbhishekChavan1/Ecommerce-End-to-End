"""
Selenium Test Configuration and Base Classes.
Provides base classes and configuration for Selenium WebDriver tests.

Quality Management Principles:
- Page Object Model: Separation of test logic from page structure
- Reusability: Base classes for common functionality
- Maintainability: Centralized WebDriver configuration
- Cross-browser Support: Configurable browser selection
"""

import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BaseSeleniumTest:
    """Base class for Selenium tests with common functionality."""
    
    @classmethod
    def setup_class(cls):
        """Set up WebDriver before running tests."""
        cls.driver = cls.get_driver()
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.base_url = "http://localhost:5000"
    
    @classmethod
    def teardown_class(cls):
        """Clean up WebDriver after tests."""
        if hasattr(cls, 'driver'):
            cls.driver.quit()
    
    @classmethod
    def get_driver(cls):
        """Get configured WebDriver instance."""
        chrome_options = Options()
        
        # Configure Chrome options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Run headless in CI environment
        if os.getenv('CI') or os.getenv('HEADLESS', 'false').lower() == 'true':
            chrome_options.add_argument("--headless")
        
        # Use local Chrome browser from fa2 folder if available
        chrome_browser_path = r"C:\Users\HP\Desktop\stqa\fa2\chrome\win64-139.0.7258.154\chrome-win64\chrome.exe"
        
        # Set Chrome binary location if local Chrome exists
        if os.path.exists(chrome_browser_path):
            chrome_options.binary_location = chrome_browser_path
        
        # Use ChromeDriverManager to automatically download the appropriate ChromeDriver
        service = Service(ChromeDriverManager().install())
        
        return webdriver.Chrome(service=service, options=chrome_options)
    
    def wait_for_element(self, locator, timeout=10):
        """Wait for element to be present and visible."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_clickable(self, locator, timeout=10):
        """Wait for element to be clickable."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    def wait_for_text_in_element(self, locator, text, timeout=10):
        """Wait for specific text to appear in element."""
        return WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )
    
    def is_element_present(self, locator):
        """Check if element is present on the page."""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def scroll_to_element(self, element):
        """Scroll to make element visible."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Brief pause for smooth scrolling
    
    def take_screenshot(self, name):
        """Take screenshot for debugging."""
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        filename = f"{screenshot_dir}/{name}_{int(time.time())}.png"
        self.driver.save_screenshot(filename)
        return filename


class BasePage:
    """Base page object class with common page functionality."""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def navigate_to(self, url):
        """Navigate to specific URL."""
        self.driver.get(url)
    
    def get_current_url(self):
        """Get current page URL."""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get page title."""
        return self.driver.title
    
    def wait_for_page_load(self):
        """Wait for page to finish loading."""
        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
    
    def find_element(self, locator):
        """Find element by locator."""
        return self.driver.find_element(*locator)
    
    def find_elements(self, locator):
        """Find multiple elements by locator."""
        return self.driver.find_elements(*locator)
    
    def click_element(self, locator):
        """Click element after waiting for it to be clickable."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator, text):
        """Enter text in input field."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Get text from element."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text
    
    def is_element_visible(self, locator):
        """Check if element is visible."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_alert_and_accept(self):
        """Wait for alert and accept it."""
        alert = self.wait.until(EC.alert_is_present())
        alert.accept()
    
    def get_alert_text(self):
        """Get alert text."""
        alert = self.wait.until(EC.alert_is_present())
        return alert.text
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def scroll_to_top(self):
        """Scroll to top of page."""
        self.driver.execute_script("window.scrollTo(0, 0);")
    
    # Common navigation elements
    @property
    def navbar_brand(self):
        return (By.CLASS_NAME, "navbar-brand")
    
    @property
    def search_input(self):
        return (By.NAME, "q")
    
    @property
    def search_button(self):
        return (By.CSS_SELECTOR, "button[type='submit']")
    
    @property
    def cart_link(self):
        return (By.XPATH, "//a[contains(@href, '/shop/cart')]")
    
    @property
    def login_link(self):
        return (By.XPATH, "//a[contains(@href, '/auth/login')]")
    
    @property
    def register_link(self):
        return (By.XPATH, "//a[contains(@href, '/auth/register')]")
    
    @property
    def logout_link(self):
        return (By.XPATH, "//a[contains(@href, '/auth/logout')]")
    
    @property
    def flash_messages(self):
        return (By.CLASS_NAME, "alert")
    
    def navigate_to_login(self):
        """Navigate to login page."""
        self.click_element(self.login_link)
    
    def navigate_to_register(self):
        """Navigate to register page."""
        self.click_element(self.register_link)
    
    def navigate_to_cart(self):
        """Navigate to cart page."""
        self.click_element(self.cart_link)
    
    def perform_search(self, query):
        """Perform search from navigation."""
        self.enter_text(self.search_input, query)
        self.click_element(self.search_button)
    
    def get_flash_message_text(self):
        """Get flash message text."""
        try:
            return self.get_text(self.flash_messages)
        except TimeoutException:
            return None
    
    def logout(self):
        """Logout current user."""
        if self.is_element_visible(self.logout_link):
            self.click_element(self.logout_link)


# Test Data Classes
class TestUser:
    """Test user data container."""
    
    def __init__(self, username="testuser", email="test@example.com", 
                 password="TestPassword123", first_name="Test", last_name="User"):
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = f"{first_name} {last_name}"


class TestProduct:
    """Test product data container."""
    
    def __init__(self, name="Test Product", price=99.99, description="Test product description"):
        self.name = name
        self.price = price
        self.description = description


# Fixtures for Selenium tests
@pytest.fixture(scope="class")
def selenium_driver():
    """Provide WebDriver instance for tests."""
    driver = BaseSeleniumTest.get_driver()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def base_page(selenium_driver):
    """Provide base page object."""
    return BasePage(selenium_driver)


@pytest.fixture
def test_user():
    """Provide test user data."""
    return TestUser()


@pytest.fixture
def admin_user():
    """Provide admin user data."""
    return TestUser(
        username="admin",
        email="admin@example.com",
        password="AdminPassword123",
        first_name="Admin",
        last_name="User"
    )


@pytest.fixture
def test_product():
    """Provide test product data."""
    return TestProduct()


# Utility functions for Selenium tests
def wait_for_page_load(driver, timeout=10):
    """Wait for page to fully load."""
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def safe_click(driver, locator, timeout=10):
    """Safely click element with explicit wait."""
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )
    element.click()


def safe_send_keys(driver, locator, text, timeout=10):
    """Safely send keys to element with explicit wait."""
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )
    element.clear()
    element.send_keys(text)
"""
Pytest configuration and fixtures for E-commerce Selenium tests.
Provides shared fixtures and test configuration.
"""

import pytest
import os
import sys
from datetime import datetime

# Add app to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.selenium.test_fixtures import TestConfig, TestData, TestUtils


def pytest_configure(config):
    """Configure pytest for Selenium tests."""
    # Create necessary directories
    TestConfig.create_directories()
    
    # Set test markers
    config.addinivalue_line("markers", "selenium: Selenium WebDriver tests")
    config.addinivalue_line("markers", "smoke: Critical functionality tests")
    config.addinivalue_line("markers", "regression: Regression tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers."""
    for item in items:
        # Add selenium marker to all tests in selenium directory
        if "selenium" in str(item.fspath):
            item.add_marker(pytest.mark.selenium)
        
        # Add smoke marker to critical tests
        if any(keyword in item.name for keyword in ["login", "cart", "checkout", "home"]):
            item.add_marker(pytest.mark.smoke)


@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration."""
    return TestConfig


@pytest.fixture(scope="session")
def test_data():
    """Provide test data."""
    return TestData


@pytest.fixture(scope="function")
def test_utils():
    """Provide test utilities."""
    return TestUtils


@pytest.fixture(scope="function")
def unique_user_data():
    """Generate unique user data for testing."""
    return {
        'username': TestUtils.generate_unique_username(),
        'email': TestUtils.generate_unique_email(),
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'testpass123'
    }


@pytest.fixture(scope="function")
def shipping_info():
    """Provide shipping information for checkout tests."""
    return TestData.SHIPPING_INFO.copy()


@pytest.fixture(scope="function")
def cart_test_data():
    """Provide cart test scenarios."""
    return TestData.CART_SCENARIOS.copy()


@pytest.fixture(autouse=True)
def test_environment_setup():
    """Setup test environment before each test."""
    # Ensure Flask app is running
    yield
    # Cleanup after test if needed


def pytest_runtest_makereport(item, call):
    """Hook to capture test results for reporting."""
    if call.when == "call":
        # Take screenshot on failure for Selenium tests
        if hasattr(item, "funcargs") and "selenium" in item.keywords:
            if call.excinfo is not None:  # Test failed
                driver = None
                # Try to get driver from test instance
                if hasattr(item.instance, 'driver'):
                    driver = item.instance.driver
                
                if driver:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_name = f"failed_{item.name}_{timestamp}.png"
                    TestUtils.take_screenshot(driver, screenshot_name)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment for entire test session."""
    print("\n" + "="*60)
    print("SETTING UP E-COMMERCE TEST ENVIRONMENT")
    print("="*60)
    
    # Verify Flask app is accessible
    import requests
    try:
        response = requests.get(TestConfig.BASE_URL, timeout=5)
        if response.status_code == 200:
            print(f"✓ Flask app is running at {TestConfig.BASE_URL}")
        else:
            print(f"⚠ Flask app returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Flask app is not accessible: {e}")
        print("Please ensure the Flask app is running with: python run.py")
        pytest.exit("Flask app is not running", returncode=1)
    
    yield
    
    print("\n" + "="*60)
    print("TEST ENVIRONMENT CLEANUP COMPLETED")
    print("="*60)


# Custom markers for test categorization
pytest_plugins = []
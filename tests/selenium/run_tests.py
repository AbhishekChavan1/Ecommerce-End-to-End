"""
Test runner for Selenium E-commerce tests.
Provides convenient test execution with proper setup and reporting.
"""

import pytest
import sys
import os
from datetime import datetime

# Add app directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def run_all_tests():
    """Run all Selenium tests with comprehensive reporting."""
    print("=" * 60)
    print("E-COMMERCE SELENIUM TEST SUITE")
    print("=" * 60)
    print(f"Test execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test arguments
    args = [
        "tests/selenium/test_ecommerce_ui.py",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--strict-markers",  # Strict marker handling
        "-x",  # Stop on first failure (optional)
        "--capture=no",  # Show print statements
        f"--html=tests/selenium/reports/test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
        "--self-contained-html"
    ]
    
    # Create reports directory
    os.makedirs("tests/selenium/reports", exist_ok=True)
    
    # Run tests
    exit_code = pytest.main(args)
    
    print()
    print("=" * 60)
    print(f"Test execution completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Exit code: {exit_code}")
    print("=" * 60)
    
    return exit_code


def run_specific_test_class(test_class):
    """Run specific test class."""
    args = [
        f"tests/selenium/test_ecommerce_ui.py::{test_class}",
        "-v",
        "--tb=short",
        "--capture=no"
    ]
    
    return pytest.main(args)


def run_authentication_tests():
    """Run only authentication tests."""
    return run_specific_test_class("TestUserAuthentication")


def run_product_tests():
    """Run only product browsing tests."""
    return run_specific_test_class("TestProductBrowsing")


def run_cart_tests():
    """Run only cart functionality tests."""
    return run_specific_test_class("TestShoppingCart")


def run_checkout_tests():
    """Run only checkout process tests."""
    return run_specific_test_class("TestCheckoutProcess")


def run_responsive_tests():
    """Run only responsive design tests."""
    return run_specific_test_class("TestResponsiveDesign")


def run_error_handling_tests():
    """Run only error handling tests."""
    return run_specific_test_class("TestErrorHandling")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="E-commerce Selenium Test Runner")
    parser.add_argument(
        "--test-group", 
        choices=[
            "all", "auth", "products", "cart", 
            "checkout", "responsive", "errors"
        ],
        default="all",
        help="Test group to run"
    )
    parser.add_argument("--headless", action="store_true", help="Run tests in headless mode")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Set environment variables for test configuration
    if args.headless:
        os.environ["HEADLESS"] = "1"
    
    # Run appropriate test group
    if args.test_group == "all":
        exit_code = run_all_tests()
    elif args.test_group == "auth":
        exit_code = run_authentication_tests()
    elif args.test_group == "products":
        exit_code = run_product_tests()
    elif args.test_group == "cart":
        exit_code = run_cart_tests()
    elif args.test_group == "checkout":
        exit_code = run_checkout_tests()
    elif args.test_group == "responsive":
        exit_code = run_responsive_tests()
    elif args.test_group == "errors":
        exit_code = run_error_handling_tests()
    
    sys.exit(exit_code)
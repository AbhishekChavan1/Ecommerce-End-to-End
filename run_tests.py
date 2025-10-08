#!/usr/bin/env python3
"""
Test Runner for E-commerce Application.
Executes comprehensive test suite including unit tests and Selenium tests.

Usage:
    python run_tests.py --unit              # Run only unit tests
    python run_tests.py --selenium          # Run only Selenium tests
    python run_tests.py --all               # Run all tests (default)
    python run_tests.py --coverage          # Run with coverage report
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


def run_unit_tests(verbose=False, coverage=False):
    """Run unit tests with pytest."""
    print("🧪 Running Unit Tests...")
    print("=" * 50)
    
    cmd = ["python", "-m", "pytest", "tests/unit/", "-v"]
    
    if coverage:
        cmd.extend(["--cov=app", "--cov-report=html", "--cov-report=term"])
    
    if verbose:
        cmd.append("-s")
    
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running unit tests: {e}")
        return False


def run_selenium_tests(verbose=False, headless=True):
    """Run Selenium tests."""
    print("🌐 Running Selenium Tests...")
    print("=" * 50)
    
    # Set environment variables for Selenium
    env = os.environ.copy()
    if headless:
        env['HEADLESS'] = 'true'
    
    cmd = ["python", "-m", "pytest", "tests/selenium/", "-v", "--tb=short"]
    
    if verbose:
        cmd.append("-s")
    
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent, env=env, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running Selenium tests: {e}")
        return False


def check_environment():
    """Check if testing environment is ready."""
    print("🔍 Checking Test Environment...")
    
    # Check if Chrome is available
    try:
        subprocess.run(["google-chrome", "--version"], capture_output=True, check=True)
        print("✅ Chrome browser available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(["chromium", "--version"], capture_output=True, check=True)
            print("✅ Chromium browser available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Warning: Chrome/Chromium not found. Selenium tests may fail.")
    
    # Check if Flask app can start
    print("✅ Environment check complete")
    print()


def display_test_summary(unit_passed, selenium_passed):
    """Display test results summary."""
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    print(f"Unit Tests:     {'✅ PASSED' if unit_passed else '❌ FAILED'}")
    print(f"Selenium Tests: {'✅ PASSED' if selenium_passed else '❌ FAILED'}")
    
    if unit_passed and selenium_passed:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("Your e-commerce application is working correctly!")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("Please review the test output above for details.")
    
    print("=" * 60)


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description='Run e-commerce application tests')
    parser.add_argument('--unit', action='store_true', help='Run only unit tests')
    parser.add_argument('--selenium', action='store_true', help='Run only Selenium tests')
    parser.add_argument('--all', action='store_true', default=True, help='Run all tests')
    parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--headed', action='store_true', help='Run Selenium tests in headed mode')
    
    args = parser.parse_args()
    
    # If specific test type is chosen, turn off --all
    if args.unit or args.selenium:
        args.all = False
    
    print("🚀 E-COMMERCE APPLICATION TEST SUITE")
    print("=" * 60)
    
    check_environment()
    
    unit_passed = True
    selenium_passed = True
    
    # Run unit tests
    if args.all or args.unit:
        unit_passed = run_unit_tests(verbose=args.verbose, coverage=args.coverage)
        print()
    
    # Run Selenium tests
    if args.all or args.selenium:
        selenium_passed = run_selenium_tests(verbose=args.verbose, headless=not args.headed)
        print()
    
    # Display summary
    if args.all:
        display_test_summary(unit_passed, selenium_passed)
    
    # Exit with appropriate code
    if (args.all and unit_passed and selenium_passed) or \
       (args.unit and unit_passed) or \
       (args.selenium and selenium_passed):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
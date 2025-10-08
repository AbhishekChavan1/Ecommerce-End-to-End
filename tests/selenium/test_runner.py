"""
Comprehensive test execution script for E-commerce Selenium tests.
Automatically starts Flask app, runs tests, and provides detailed reporting.
"""

import subprocess
import sys
import os
import time
import requests
import signal
from contextlib import contextmanager
from datetime import datetime

# Add app directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestRunner:
    """Manages test execution with Flask app lifecycle."""
    
    def __init__(self):
        self.flask_process = None
        self.base_url = "http://localhost:5000"
        self.max_startup_wait = 30  # seconds
    
    @contextmanager
    def flask_app(self):
        """Context manager for Flask app lifecycle."""
        self.start_flask_app()
        try:
            yield
        finally:
            self.stop_flask_app()
    
    def start_flask_app(self):
        """Start Flask application."""
        print("Starting Flask application...")
        
        # Check if app is already running
        if self.is_app_running():
            print("✓ Flask app is already running")
            return
        
        # Start Flask app
        try:
            self.flask_process = subprocess.Popen(
                [sys.executable, "run.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
            )
            
            # Wait for app to start
            start_time = time.time()
            while time.time() - start_time < self.max_startup_wait:
                if self.is_app_running():
                    print("✓ Flask app started successfully")
                    time.sleep(2)  # Additional wait for full initialization
                    return
                time.sleep(1)
            
            raise Exception("Flask app failed to start within timeout")
            
        except Exception as e:
            print(f"✗ Failed to start Flask app: {e}")
            self.stop_flask_app()
            raise
    
    def stop_flask_app(self):
        """Stop Flask application."""
        if self.flask_process and self.flask_process.poll() is None:
            print("Stopping Flask application...")
            self.flask_process.terminate()
            try:
                self.flask_process.wait(timeout=5)
                print("✓ Flask app stopped")
            except subprocess.TimeoutExpired:
                self.flask_process.kill()
                print("✓ Flask app force-stopped")
            self.flask_process = None
    
    def is_app_running(self):
        """Check if Flask app is running."""
        try:
            response = requests.get(self.base_url, timeout=3)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def run_tests(self, test_args=None):
        """Run tests with Flask app context."""
        if test_args is None:
            test_args = []
        
        print("=" * 80)
        print("E-COMMERCE SELENIUM TEST SUITE")
        print("=" * 80)
        print(f"Test execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        with self.flask_app():
            # Verify app is accessible
            if not self.is_app_running():
                print("✗ Flask app is not accessible")
                return 1
            
            print(f"✓ Flask app is accessible at {self.base_url}")
            print()
            
            # Set up test environment
            os.makedirs("tests/selenium/reports", exist_ok=True)
            os.makedirs("tests/selenium/screenshots", exist_ok=True)
            
            # Default test arguments
            default_args = [
                "tests/selenium/test_ecommerce_ui.py",
                "-v",
                "--tb=short",
                "--strict-markers",
                "--capture=no",
                f"--html=tests/selenium/reports/test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                "--self-contained-html"
            ]
            
            # Merge with provided arguments
            final_args = default_args + test_args
            
            # Import pytest and run
            import pytest
            exit_code = pytest.main(final_args)
            
            print()
            print("=" * 80)
            print(f"Test execution completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Exit code: {exit_code}")
            print("=" * 80)
            
            return exit_code


def main():
    """Main entry point for test execution."""
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
    parser.add_argument("--stop-on-failure", action="store_true", help="Stop on first failure")
    parser.add_argument("--parallel", type=int, help="Run tests in parallel (number of workers)")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    
    args = parser.parse_args()
    
    # Set environment variables for test configuration
    if args.headless:
        os.environ["HEADLESS"] = "1"
    
    # Build test arguments
    test_args = []
    
    # Test selection
    if args.test_group != "all":
        test_args.extend(["-k", args.test_group])
    
    # Stop on first failure
    if args.stop_on_failure:
        test_args.append("-x")
    
    # Parallel execution
    if args.parallel:
        test_args.extend(["-n", str(args.parallel)])
    
    # Coverage
    if args.coverage:
        test_args.extend([
            "--cov=app",
            "--cov-report=html:tests/selenium/reports/coverage",
            "--cov-report=term-missing"
        ])
    
    # Run tests
    runner = TestRunner()
    
    def signal_handler(signum, frame):
        print("\nReceived interrupt signal. Cleaning up...")
        runner.stop_flask_app()
        sys.exit(1)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        exit_code = runner.run_tests(test_args)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nTest execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error during test execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
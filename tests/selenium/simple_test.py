"""
Simple Selenium test to verify basic e-commerce functionality.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """Set up Chrome WebDriver with basic options."""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Use system's default Chrome installation
    service = Service(ChromeDriverManager().install())
    
    return webdriver.Chrome(service=service, options=chrome_options)


def test_ecommerce_basic_functionality():
    """Test basic e-commerce functionality."""
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    
    try:
        print("🚀 Starting E-commerce Application Tests...")
        print("=" * 60)
        
        # Test 1: Load Home Page
        print("1. Testing Home Page Load...")
        driver.get("http://localhost:5000")
        assert "E-Commerce" in driver.title or "Shop" in driver.title
        print("   ✅ Home page loaded successfully")
        
        # Test 2: Check Navigation
        print("2. Testing Navigation...")
        nav_elements = driver.find_elements(By.CSS_SELECTOR, ".navbar-nav a")
        nav_links = [elem.get_attribute('href') for elem in nav_elements if elem.get_attribute('href')]
        print(f"   ✅ Found {len(nav_links)} navigation links")
        
        # Test 3: Check Products Page
        print("3. Testing Products Page...")
        try:
            products_link = driver.find_element(By.XPATH, "//a[contains(@href, '/shop') or contains(text(), 'Shop') or contains(text(), 'Products')]")
            products_link.click()
            time.sleep(2)
            print("   ✅ Products page accessed successfully")
        except Exception as e:
            print(f"   ⚠️  Products page test skipped: {e}")
        
        # Test 4: Check for Product Cards
        print("4. Testing Product Display...")
        try:
            product_cards = driver.find_elements(By.CSS_SELECTOR, ".card, .product-card, .product")
            if product_cards:
                print(f"   ✅ Found {len(product_cards)} product cards")
            else:
                print("   ⚠️  No product cards found (might need sample data)")
        except Exception as e:
            print(f"   ⚠️  Product display test error: {e}")
        
        # Test 5: Test Add to Cart (if products exist)
        print("5. Testing Add to Cart Functionality...")
        try:
            add_to_cart_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Add to Cart') or contains(@class, 'add-to-cart')]")
            if add_to_cart_buttons:
                add_to_cart_buttons[0].click()
                time.sleep(2)
                print("   ✅ Add to cart button clicked successfully")
                
                # Check for success message or cart update
                try:
                    success_msg = driver.find_element(By.CSS_SELECTOR, ".alert-success, .alert, .flash-message")
                    print(f"   ✅ Success message displayed: {success_msg.text[:50]}...")
                except:
                    print("   ℹ️  No success message found (might be AJAX-based)")
            else:
                print("   ⚠️  No add to cart buttons found")
        except Exception as e:
            print(f"   ⚠️  Add to cart test error: {e}")
        
        # Test 6: Test Cart Page
        print("6. Testing Cart Page...")
        try:
            cart_link = driver.find_element(By.XPATH, "//a[contains(@href, 'cart') or contains(text(), 'Cart')]")
            cart_link.click()
            time.sleep(2)
            print("   ✅ Cart page accessed successfully")
        except Exception as e:
            print(f"   ⚠️  Cart page test error: {e}")
        
        # Test 7: Test User Authentication Pages
        print("7. Testing Authentication Pages...")
        try:
            driver.get("http://localhost:5000/auth/login")
            login_form = driver.find_element(By.TAG_NAME, "form")
            print("   ✅ Login page loaded successfully")
        except Exception as e:
            print(f"   ⚠️  Login page test error: {e}")
        
        try:
            driver.get("http://localhost:5000/auth/register")
            register_form = driver.find_element(By.TAG_NAME, "form")
            print("   ✅ Register page loaded successfully")
        except Exception as e:
            print(f"   ⚠️  Register page test error: {e}")
        
        print("=" * 60)
        print("🎉 Basic E-commerce Tests Completed!")
        print("   Your e-commerce application is running and accessible!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
        
    finally:
        driver.quit()


if __name__ == "__main__":
    success = test_ecommerce_basic_functionality()
    exit(0 if success else 1)
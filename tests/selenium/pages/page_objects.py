"""
Page Object Model classes for E-commerce Application.
Implements page-specific functionality following Page Object Model pattern.

Quality Management Principles:
- Encapsulation: Page-specific logic contained in respective classes
- Reusability: Common actions available for test methods
- Maintainability: Locators and actions centralized per page
- Abstraction: Test logic separated from UI implementation details
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from tests.selenium.base import BasePage
import time


class HomePage(BasePage):
    """Home page object with hero section and featured products."""
    
    # Locators
    HERO_SECTION = (By.CLASS_NAME, "hero-section")
    HERO_TITLE = (By.CSS_SELECTOR, ".hero-section h1")
    HERO_SUBTITLE = (By.CSS_SELECTOR, ".hero-section p")
    SHOP_NOW_BUTTON = (By.XPATH, "//a[contains(text(), 'Shop Now')]")
    FEATURED_PRODUCTS = (By.CLASS_NAME, "featured-products")
    PRODUCT_CARDS = (By.CLASS_NAME, "product-card")
    CATEGORIES_SECTION = (By.CLASS_NAME, "categories-section")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:5000/"
    
    def navigate_to_home(self):
        """Navigate to home page."""
        self.navigate_to(self.url)
        self.wait_for_page_load()
    
    def is_hero_section_visible(self):
        """Check if hero section is visible."""
        return self.is_element_visible(self.HERO_SECTION)
    
    def get_hero_title(self):
        """Get hero section title text."""
        try:
            return self.get_text(self.HERO_TITLE)
        except TimeoutException:
            return ""
    
    def get_hero_subtitle(self):
        """Get hero section subtitle text."""
        try:
            return self.get_text(self.HERO_SUBTITLE)
        except TimeoutException:
            return ""
    
    def click_shop_now(self):
        """Click shop now button."""
        self.click_element(self.SHOP_NOW_BUTTON)
    
    def get_featured_products_count(self):
        """Get number of featured products displayed."""
        products = self.find_elements(self.PRODUCT_CARDS)
        return len(products)
    
    def click_featured_product(self, index=0):
        """Click on featured product by index."""
        products = self.find_elements(self.PRODUCT_CARDS)
        if index < len(products):
            products[index].click()
    
    def is_categories_section_visible(self):
        """Check if categories section is visible."""
        return self.is_element_visible(self.CATEGORIES_SECTION)


class LoginPage(BasePage):
    """Login page object with authentication functionality."""
    
    # Locators
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    REGISTER_LINK = (By.XPATH, "//a[contains(@href, '/auth/register')]")
    ERROR_MESSAGES = (By.CLASS_NAME, "alert-danger")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(text(), 'Forgot Password')]")
    LOGIN_FORM = (By.CSS_SELECTOR, "form")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:5000/auth/login"
    
    def navigate_to_login(self):
        """Navigate to login page."""
        self.navigate_to(self.url)
        self.wait_for_page_load()
    
    def is_login_form_visible(self):
        """Check if login form is visible."""
        return self.is_element_visible(self.LOGIN_FORM)
    
    def enter_username(self, username):
        """Enter username in login form."""
        self.enter_text(self.USERNAME_FIELD, username)
    
    def enter_password(self, password):
        """Enter password in login form."""
        self.enter_text(self.PASSWORD_FIELD, password)
    
    def click_login(self):
        """Click login button."""
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username, password):
        """Complete login process."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        time.sleep(2)  # Wait for form submission
    
    def click_register_link(self):
        """Click register link."""
        self.click_element(self.REGISTER_LINK)
    
    def get_error_messages(self):
        """Get error message texts."""
        try:
            elements = self.find_elements(self.ERROR_MESSAGES)
            return [element.text for element in elements]
        except NoSuchElementException:
            return []
    
    def is_forgot_password_visible(self):
        """Check if forgot password link is visible."""
        return self.is_element_visible(self.FORGOT_PASSWORD_LINK)


class RegisterPage(BasePage):
    """Registration page object with user signup functionality."""
    
    # Locators
    FIRST_NAME_FIELD = (By.ID, "first_name")
    LAST_NAME_FIELD = (By.ID, "last_name")
    USERNAME_FIELD = (By.ID, "username")
    EMAIL_FIELD = (By.ID, "email")
    PASSWORD_FIELD = (By.ID, "password")
    CONFIRM_PASSWORD_FIELD = (By.ID, "confirm_password")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_LINK = (By.XPATH, "//a[contains(@href, '/auth/login')]")
    ERROR_MESSAGES = (By.CLASS_NAME, "alert-danger")
    SUCCESS_MESSAGES = (By.CLASS_NAME, "alert-success")
    REGISTER_FORM = (By.CSS_SELECTOR, "form")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:5000/auth/register"
    
    def navigate_to_register(self):
        """Navigate to registration page."""
        self.navigate_to(self.url)
        self.wait_for_page_load()
    
    def is_register_form_visible(self):
        """Check if registration form is visible."""
        return self.is_element_visible(self.REGISTER_FORM)
    
    def enter_first_name(self, first_name):
        """Enter first name."""
        self.enter_text(self.FIRST_NAME_FIELD, first_name)
    
    def enter_last_name(self, last_name):
        """Enter last name."""
        self.enter_text(self.LAST_NAME_FIELD, last_name)
    
    def enter_username(self, username):
        """Enter username."""
        self.enter_text(self.USERNAME_FIELD, username)
    
    def enter_email(self, email):
        """Enter email address."""
        self.enter_text(self.EMAIL_FIELD, email)
    
    def enter_password(self, password):
        """Enter password."""
        self.enter_text(self.PASSWORD_FIELD, password)
    
    def enter_confirm_password(self, password):
        """Enter password confirmation."""
        self.enter_text(self.CONFIRM_PASSWORD_FIELD, password)
    
    def click_register(self):
        """Click register button."""
        self.click_element(self.REGISTER_BUTTON)
    
    def register(self, first_name, last_name, username, email, password):
        """Complete registration process."""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_username(username)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_confirm_password(password)
        self.click_register()
        time.sleep(2)  # Wait for form submission
    
    def get_error_messages(self):
        """Get error message texts."""
        try:
            elements = self.find_elements(self.ERROR_MESSAGES)
            return [element.text for element in elements]
        except NoSuchElementException:
            return []
    
    def get_success_messages(self):
        """Get success message texts."""
        try:
            elements = self.find_elements(self.SUCCESS_MESSAGES)
            return [element.text for element in elements]
        except NoSuchElementException:
            return []


class ProductListPage(BasePage):
    """Products listing page with search and filtering."""
    
    # Locators
    SEARCH_INPUT = (By.ID, "search-input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CATEGORY_FILTER = (By.ID, "category")
    SORT_DROPDOWN = (By.ID, "sort_by")
    PRODUCT_CARDS = (By.CLASS_NAME, "product-card")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-card h5")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".product-card .price")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".product-card img")
    VIEW_DETAILS_LINKS = (By.CSS_SELECTOR, ".product-card a")
    NO_PRODUCTS_MESSAGE = (By.CLASS_NAME, "no-products")
    PAGINATION = (By.CLASS_NAME, "pagination")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:5000/shop/products"
    
    def navigate_to_products(self):
        """Navigate to products page."""
        self.navigate_to(self.url)
        self.wait_for_page_load()
    
    def search_products(self, search_term):
        """Search for products."""
        if self.is_element_visible(self.SEARCH_INPUT):
            self.enter_text(self.SEARCH_INPUT, search_term)
            self.click_element(self.SEARCH_BUTTON)
            self.wait_for_page_load()
    
    def filter_by_category(self, category_text):
        """Filter products by category."""
        if self.is_element_visible(self.CATEGORY_FILTER):
            category_dropdown = Select(self.find_element(self.CATEGORY_FILTER))
            category_dropdown.select_by_visible_text(category_text)
            self.wait_for_page_load()
    
    def sort_products(self, sort_option):
        """Sort products by specified option."""
        if self.is_element_visible(self.SORT_DROPDOWN):
            sort_dropdown = Select(self.find_element(self.SORT_DROPDOWN))
            sort_dropdown.select_by_value(sort_option)
            self.wait_for_page_load()
    
    def get_product_count(self):
        """Get number of products displayed."""
        products = self.find_elements(self.PRODUCT_CARDS)
        return len(products)
    
    def has_products(self):
        """Check if products are available."""
        return self.get_product_count() > 0
    
    def get_product_names(self):
        """Get list of product names."""
        try:
            elements = self.find_elements(self.PRODUCT_NAMES)
            return [element.text for element in elements]
        except NoSuchElementException:
            return []
    
    def get_product_prices(self):
        """Get list of product prices."""
        try:
            elements = self.find_elements(self.PRODUCT_PRICES)
            return [element.text for element in elements]
        except NoSuchElementException:
            return []
    
    def click_product(self, index=0):
        """Click on product by index."""
        products = self.find_elements(self.PRODUCT_CARDS)
        if index < len(products):
            # Find the link within the product card
            link = products[index].find_element(By.TAG_NAME, "a")
            link.click()
            self.wait_for_page_load()
    
    def is_no_products_message_visible(self):
        """Check if no products message is visible."""
        return self.is_element_visible(self.NO_PRODUCTS_MESSAGE)
    
    def is_pagination_visible(self):
        """Check if pagination is visible."""
        return self.is_element_visible(self.PAGINATION)


class ProductDetailPage(BasePage):
    """Product detail page with add to cart functionality."""
    
    # Locators
    PRODUCT_NAME = (By.CSS_SELECTOR, "h1")
    PRODUCT_PRICE = (By.CLASS_NAME, "price")
    PRODUCT_DESCRIPTION = (By.CLASS_NAME, "description")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, ".product-image img")
    QUANTITY_INPUT = (By.ID, "quantity")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    BACK_TO_PRODUCTS_LINK = (By.XPATH, "//a[contains(text(), 'Back to Products')]")
    RELATED_PRODUCTS = (By.CLASS_NAME, "related-products")
    PRODUCT_DETAILS = (By.CLASS_NAME, "product-details")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "alert-success")
    ERROR_MESSAGE = (By.CLASS_NAME, "alert-danger")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_product_name(self):
        """Get product name."""
        try:
            return self.get_text(self.PRODUCT_NAME)
        except TimeoutException:
            return ""
    
    def get_product_price(self):
        """Get product price."""
        try:
            return self.get_text(self.PRODUCT_PRICE)
        except TimeoutException:
            return ""
    
    def get_product_description(self):
        """Get product description."""
        try:
            return self.get_text(self.PRODUCT_DESCRIPTION)
        except TimeoutException:
            return ""
    
    def is_product_image_visible(self):
        """Check if product image is visible."""
        return self.is_element_visible(self.PRODUCT_IMAGE)
    
    def set_quantity(self, quantity):
        """Set product quantity."""
        if self.is_element_visible(self.QUANTITY_INPUT):
            self.enter_text(self.QUANTITY_INPUT, str(quantity))
    
    def click_add_to_cart(self):
        """Click add to cart button."""
        self.click_element(self.ADD_TO_CART_BUTTON)
        time.sleep(2)  # Wait for AJAX request
    
    def add_to_cart(self, quantity=1):
        """Add product to cart with specified quantity."""
        self.set_quantity(quantity)
        self.click_add_to_cart()
    
    def is_add_to_cart_enabled(self):
        """Check if add to cart button is enabled."""
        try:
            button = self.find_element(self.ADD_TO_CART_BUTTON)
            return button.is_enabled()
        except NoSuchElementException:
            return False
    
    def click_back_to_products(self):
        """Click back to products link."""
        if self.is_element_visible(self.BACK_TO_PRODUCTS_LINK):
            self.click_element(self.BACK_TO_PRODUCTS_LINK)
    
    def is_related_products_visible(self):
        """Check if related products section is visible."""
        return self.is_element_visible(self.RELATED_PRODUCTS)
    
    def get_success_message(self):
        """Get success message text."""
        try:
            return self.get_text(self.SUCCESS_MESSAGE)
        except TimeoutException:
            return ""
    
    def get_error_message(self):
        """Get error message text."""
        try:
            return self.get_text(self.ERROR_MESSAGE)
        except TimeoutException:
            return ""


class CartPage(BasePage):
    """Shopping cart page with cart management functionality."""
    
    # Locators
    CART_ITEMS = (By.CLASS_NAME, "cart-item")
    ITEM_NAMES = (By.CSS_SELECTOR, ".cart-item h6")
    ITEM_QUANTITIES = (By.CSS_SELECTOR, ".cart-item input[name='quantity']")
    ITEM_PRICES = (By.CSS_SELECTOR, ".cart-item .price")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, ".cart-item .btn-danger")
    UPDATE_BUTTONS = (By.CSS_SELECTOR, ".cart-item button[type='submit']")
    CONTINUE_SHOPPING_BUTTON = (By.XPATH, "//a[contains(text(), 'Continue Shopping')]")
    CHECKOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'Checkout')]")
    CLEAR_CART_BUTTON = (By.XPATH, "//a[contains(text(), 'Clear Cart')]")
    CART_TOTAL = (By.CLASS_NAME, "cart-total")
    EMPTY_CART_MESSAGE = (By.XPATH, "//h3[contains(text(), 'Your cart is empty')]")
    CART_SUMMARY = (By.CLASS_NAME, "cart-summary")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:5000/shop/cart"
    
    def navigate_to_cart(self):
        """Navigate to cart page."""
        self.navigate_to(self.url)
        self.wait_for_page_load()
    
    def is_cart_empty(self):
        """Check if cart is empty."""
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)
    
    def get_cart_item_count(self):
        """Get number of items in cart."""
        items = self.find_elements(self.CART_ITEMS)
        return len(items)
    
    def get_item_names(self):
        """Get list of item names in cart."""
        try:
            elements = self.find_elements(self.ITEM_NAMES)
            return [element.text for element in elements]
        except NoSuchElementException:
            return []
    
    def get_item_quantities(self):
        """Get list of item quantities."""
        try:
            elements = self.find_elements(self.ITEM_QUANTITIES)
            return [int(element.get_attribute('value')) for element in elements]
        except (NoSuchElementException, ValueError):
            return []
    
    def update_item_quantity(self, item_index, new_quantity):
        """Update quantity of specific cart item."""
        quantity_inputs = self.find_elements(self.ITEM_QUANTITIES)
        if item_index < len(quantity_inputs):
            quantity_input = quantity_inputs[item_index]
            quantity_input.clear()
            quantity_input.send_keys(str(new_quantity))
            
            # Find and click corresponding update button
            update_buttons = self.find_elements(self.UPDATE_BUTTONS)
            if item_index < len(update_buttons):
                update_buttons[item_index].click()
                time.sleep(2)  # Wait for update
    
    def remove_item(self, item_index):
        """Remove specific cart item."""
        remove_buttons = self.find_elements(self.REMOVE_BUTTONS)
        if item_index < len(remove_buttons):
            remove_buttons[item_index].click()
            time.sleep(2)  # Wait for removal
    
    def click_continue_shopping(self):
        """Click continue shopping button."""
        if self.is_element_visible(self.CONTINUE_SHOPPING_BUTTON):
            self.click_element(self.CONTINUE_SHOPPING_BUTTON)
    
    def click_checkout(self):
        """Click checkout button."""
        if self.is_element_visible(self.CHECKOUT_BUTTON):
            self.click_element(self.CHECKOUT_BUTTON)
            self.wait_for_page_load()
    
    def is_checkout_button_visible(self):
        """Check if checkout button is visible."""
        return self.is_element_visible(self.CHECKOUT_BUTTON)
    
    def click_clear_cart(self):
        """Click clear cart button."""
        if self.is_element_visible(self.CLEAR_CART_BUTTON):
            self.click_element(self.CLEAR_CART_BUTTON)
            # Handle confirmation dialog if present
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
            except:
                pass
            time.sleep(2)  # Wait for clearing
    
    def get_cart_total(self):
        """Get cart total amount."""
        try:
            return self.get_text(self.CART_TOTAL)
        except TimeoutException:
            return ""
    
    def is_cart_summary_visible(self):
        """Check if cart summary is visible."""
        return self.is_element_visible(self.CART_SUMMARY)


class CheckoutPage(BasePage):
    """Checkout page with order completion functionality."""
    
    # Locators
    SHIPPING_FIRST_NAME = (By.ID, "shipping_first_name")
    SHIPPING_LAST_NAME = (By.ID, "shipping_last_name")
    SHIPPING_EMAIL = (By.ID, "shipping_email")
    SHIPPING_PHONE = (By.ID, "shipping_phone")
    SHIPPING_ADDRESS_LINE1 = (By.ID, "shipping_address_line1")
    SHIPPING_ADDRESS_LINE2 = (By.ID, "shipping_address_line2")
    SHIPPING_CITY = (By.ID, "shipping_city")
    SHIPPING_STATE = (By.ID, "shipping_state")
    SHIPPING_POSTAL_CODE = (By.ID, "shipping_postal_code")
    SHIPPING_COUNTRY = (By.ID, "shipping_country")
    PAYMENT_METHOD = (By.ID, "payment_method")
    ORDER_NOTES = (By.ID, "notes")
    PLACE_ORDER_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FILL_DEMO_DATA_BUTTON = (By.XPATH, "//button[contains(text(), 'Fill Demo Data')]")
    ORDER_SUMMARY = (By.CLASS_NAME, "order-summary")
    CHECKOUT_FORM = (By.CSS_SELECTOR, "form")
    BACK_TO_CART_LINK = (By.XPATH, "//a[contains(@href, '/shop/cart')]")
    ERROR_MESSAGES = (By.CLASS_NAME, "alert-danger")
    SUCCESS_MESSAGES = (By.CLASS_NAME, "alert-success")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:5000/shop/checkout"
    
    def navigate_to_checkout(self):
        """Navigate to checkout page."""
        self.navigate_to(self.url)
        self.wait_for_page_load()
    
    def is_checkout_form_visible(self):
        """Check if checkout form is visible."""
        return self.is_element_visible(self.CHECKOUT_FORM)
    
    def fill_shipping_info(self, shipping_info):
        """Fill shipping information form."""
        if 'first_name' in shipping_info:
            self.enter_text(self.SHIPPING_FIRST_NAME, shipping_info['first_name'])
        if 'last_name' in shipping_info:
            self.enter_text(self.SHIPPING_LAST_NAME, shipping_info['last_name'])
        if 'email' in shipping_info:
            self.enter_text(self.SHIPPING_EMAIL, shipping_info['email'])
        if 'phone' in shipping_info:
            self.enter_text(self.SHIPPING_PHONE, shipping_info['phone'])
        if 'address' in shipping_info:
            self.enter_text(self.SHIPPING_ADDRESS_LINE1, shipping_info['address'])
        if 'address2' in shipping_info:
            self.enter_text(self.SHIPPING_ADDRESS_LINE2, shipping_info['address2'])
        if 'city' in shipping_info:
            self.enter_text(self.SHIPPING_CITY, shipping_info['city'])
        if 'state' in shipping_info:
            self.enter_text(self.SHIPPING_STATE, shipping_info['state'])
        if 'postal_code' in shipping_info:
            self.enter_text(self.SHIPPING_POSTAL_CODE, shipping_info['postal_code'])
        if 'country' in shipping_info:
            self.enter_text(self.SHIPPING_COUNTRY, shipping_info['country'])
    
    def select_payment_method(self, payment_method):
        """Select payment method."""
        if self.is_element_visible(self.PAYMENT_METHOD):
            payment_dropdown = Select(self.find_element(self.PAYMENT_METHOD))
            payment_dropdown.select_by_value(payment_method)
    
    def enter_order_notes(self, notes):
        """Enter order notes."""
        if self.is_element_visible(self.ORDER_NOTES):
            self.enter_text(self.ORDER_NOTES, notes)
    
    def click_fill_demo_data(self):
        """Click fill demo data button."""
        if self.is_element_visible(self.FILL_DEMO_DATA_BUTTON):
            self.click_element(self.FILL_DEMO_DATA_BUTTON)
            time.sleep(1)  # Wait for form to fill
    
    def click_place_order(self):
        """Click place order button."""
        self.click_element(self.PLACE_ORDER_BUTTON)
        time.sleep(3)  # Wait for order processing
    
    def complete_checkout(self, shipping_info, payment_method="credit_card", notes=""):
        """Complete entire checkout process."""
        self.fill_shipping_info(shipping_info)
        self.select_payment_method(payment_method)
        if notes:
            self.enter_order_notes(notes)
        self.click_place_order()
    
    def complete_demo_checkout(self):
        """Complete checkout using demo data."""
        self.click_fill_demo_data()
        self.click_place_order()
    
    def is_order_summary_visible(self):
        """Check if order summary is visible."""
        return self.is_element_visible(self.ORDER_SUMMARY)
    
    def click_back_to_cart(self):
        """Click back to cart link."""
        if self.is_element_visible(self.BACK_TO_CART_LINK):
            self.click_element(self.BACK_TO_CART_LINK)
    
    def get_error_messages(self):
        """Get error message texts."""
        try:
            elements = self.find_elements(self.ERROR_MESSAGES)
            return [element.text for element in elements]
        except NoSuchElementException:
            return []
    
    def get_success_messages(self):
        """Get success message texts."""
        try:
            elements = self.find_elements(self.SUCCESS_MESSAGES)
            return [element.text for element in elements]
        except NoSuchElementException:
            return []


class OrderConfirmationPage(BasePage):
    """Order confirmation page after successful checkout."""
    
    # Locators
    SUCCESS_ICON = (By.CSS_SELECTOR, ".fa-check-circle")
    ORDER_NUMBER = (By.XPATH, "//*[contains(text(), 'Order Number:')]/following-sibling::*")
    ORDER_DETAILS = (By.CLASS_NAME, "order-details")
    CONTINUE_SHOPPING_BUTTON = (By.XPATH, "//a[contains(text(), 'Continue Shopping')]")
    BACK_TO_HOME_BUTTON = (By.XPATH, "//a[contains(text(), 'Back to Home')]")
    ORDER_ITEMS = (By.CLASS_NAME, "order-items")
    ORDER_TOTAL = (By.CLASS_NAME, "order-total")
    DEMO_NOTICE = (By.CLASS_NAME, "alert-info")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_success_page_displayed(self):
        """Check if order success page is displayed."""
        return self.is_element_visible(self.SUCCESS_ICON)
    
    def get_order_number(self):
        """Get order number from confirmation page."""
        try:
            return self.get_text(self.ORDER_NUMBER)
        except TimeoutException:
            return ""
    
    def is_order_details_visible(self):
        """Check if order details are visible."""
        return self.is_element_visible(self.ORDER_DETAILS)
    
    def click_continue_shopping(self):
        """Click continue shopping button."""
        if self.is_element_visible(self.CONTINUE_SHOPPING_BUTTON):
            self.click_element(self.CONTINUE_SHOPPING_BUTTON)
    
    def click_back_to_home(self):
        """Click back to home button."""
        if self.is_element_visible(self.BACK_TO_HOME_BUTTON):
            self.click_element(self.BACK_TO_HOME_BUTTON)
    
    def is_demo_notice_visible(self):
        """Check if demo notice is visible."""
        return self.is_element_visible(self.DEMO_NOTICE)
    
    def get_demo_notice_text(self):
        """Get demo notice text."""
        try:
            return self.get_text(self.DEMO_NOTICE)
        except TimeoutException:
            return ""
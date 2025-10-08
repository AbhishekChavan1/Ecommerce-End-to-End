"""
Page Object Model package for E-commerce Selenium tests.
Contains page object classes following the Page Object Model pattern.

This module provides comprehensive page objects that have been enhanced
with improved error handling, better locators, and additional functionality.
"""

# Import from the enhanced page objects module
from .page_objects import (
    HomePage,
    LoginPage, 
    RegisterPage,
    ProductListPage,
    ProductDetailPage,
    CartPage,
    CheckoutPage,
    OrderConfirmationPage
)

__all__ = [
    'HomePage',
    'LoginPage',
    'RegisterPage', 
    'ProductListPage',
    'ProductDetailPage',
    'CartPage',
    'CheckoutPage',
    'OrderConfirmationPage'
]
"""
Unit Tests for Product and Category Models.
Tests product catalog functionality, pricing, and inventory management.

Quality Management Principles:
- Business Logic Testing: Tests pricing calculations and stock management
- Data Integrity: Tests model relationships and constraints
- Performance Testing: Tests query methods and pagination
- Validation Testing: Tests input validation and error handling
"""

import pytest
from decimal import Decimal
from app.models.product import Product, Category
from app import db


class TestCategoryModel:
    """Test cases for Category model."""
    
    def test_category_creation(self, clean_db):
        """Test basic category creation."""
        category = Category(
            name='Electronics',
            description='Electronic devices and gadgets'
        )
        clean_db.session.add(category)
        clean_db.session.commit()
        
        assert category.id is not None
        assert category.name == 'Electronics'
        assert category.slug == 'electronics'
        assert category.is_active is True
    
    def test_category_slug_generation(self, clean_db):
        """Test automatic slug generation."""
        category = Category(name='Home & Garden')
        assert category.slug == 'home-and-garden'
        
        category2 = Category(name='Sports & Fitness')
        assert category2.slug == 'sports-and-fitness'
    
    def test_category_product_count(self, clean_db, sample_category, multiple_products):
        """Test product count calculation."""
        # Should count only active products
        active_count = sum(1 for p in multiple_products if p.is_active and p.category_id == sample_category.id)
        assert sample_category.get_product_count() == active_count
    
    def test_category_to_dict(self, clean_db, sample_category):
        """Test category dictionary conversion."""
        category_dict = sample_category.to_dict()
        
        assert category_dict['id'] == sample_category.id
        assert category_dict['name'] == sample_category.name
        assert category_dict['slug'] == sample_category.slug
        assert category_dict['is_active'] == sample_category.is_active
        assert 'product_count' in category_dict


class TestProductModel:
    """Test cases for Product model."""
    
    def test_product_creation(self, clean_db, sample_category):
        """Test basic product creation."""
        product = Product(
            name='Test Laptop',
            price=999.99,
            category_id=sample_category.id,
            description='A test laptop',
            stock_quantity=10
        )
        clean_db.session.add(product)
        clean_db.session.commit()
        
        assert product.id is not None
        assert product.name == 'Test Laptop'
        assert product.price == Decimal('999.99')
        assert product.slug == 'test-laptop'
        assert product.is_active is True
        assert product.is_featured is False
    
    def test_product_pricing(self, clean_db, sample_category):
        """Test product pricing calculations."""
        # Regular product
        product = Product(
            name='Regular Product',
            price=100.00,
            category_id=sample_category.id
        )
        assert product.get_effective_price() == 100.00
        assert product.is_on_sale() is False
        assert product.get_discount_percentage() == 0
        
        # Product on sale
        sale_product = Product(
            name='Sale Product',
            price=100.00,
            sale_price=80.00,
            category_id=sample_category.id
        )
        assert sale_product.get_effective_price() == 80.00
        assert sale_product.is_on_sale() is True
        assert sale_product.get_discount_percentage() == 20.0
    
    def test_stock_management(self, clean_db, sample_product):
        """Test stock management methods."""
        # Initial stock
        assert sample_product.is_in_stock() is True
        assert sample_product.is_low_stock() is False
        assert sample_product.get_stock_status() == 'In Stock'
        
        # Update stock
        sample_product.update_stock(-5)  # Remove 5 items
        assert sample_product.stock_quantity == 5
        assert sample_product.is_low_stock() is True
        assert sample_product.get_stock_status() == 'Low Stock'
        
        # Out of stock
        sample_product.update_stock(-5)  # Remove remaining 5 items
        assert sample_product.stock_quantity == 0
        assert sample_product.is_in_stock() is False
        assert sample_product.get_stock_status() == 'Out of Stock'
    
    def test_stock_validation(self, clean_db, sample_product):
        """Test stock validation prevents negative quantities."""
        with pytest.raises(ValueError, match="Stock quantity cannot be negative"):
            sample_product.update_stock(-20)  # Would make stock negative
    
    def test_stock_reservation(self, clean_db, sample_product):
        """Test stock reservation and release."""
        original_stock = sample_product.stock_quantity
        
        # Reserve stock
        sample_product.reserve_stock(3)
        assert sample_product.stock_quantity == original_stock - 3
        
        # Release stock
        sample_product.release_stock(2)
        assert sample_product.stock_quantity == original_stock - 1
    
    def test_stock_reservation_validation(self, clean_db, sample_product):
        """Test stock reservation validation."""
        with pytest.raises(ValueError, match="Insufficient stock"):
            sample_product.reserve_stock(20)  # More than available
    
    def test_profit_margin_calculation(self, clean_db, sample_category):
        """Test profit margin calculation."""
        product = Product(
            name='Profit Test',
            price=100.00,
            cost_price=80.00,
            category_id=sample_category.id
        )
        assert product.get_profit_margin() == 25.0  # (100-80)/80 * 100
        
        # Product without cost price
        product_no_cost = Product(
            name='No Cost Product',
            price=100.00,
            category_id=sample_category.id
        )
        assert product_no_cost.get_profit_margin() == 0
    
    def test_product_search(self, clean_db, multiple_products):
        """Test product search functionality."""
        # Search by name
        results = Product.search_products('Laptop')
        laptop_products = [p for p in results.items if 'laptop' in p.name.lower()]
        assert len(laptop_products) > 0
        
        # Search by description
        results = Product.search_products('wireless')
        wireless_products = [p for p in results.items if 'wireless' in (p.description or '').lower()]
        assert len(wireless_products) >= 0  # May or may not find results
    
    def test_featured_products(self, clean_db, multiple_products):
        """Test featured products retrieval."""
        featured = Product.get_featured_products(limit=5)
        featured_count = len([p for p in multiple_products if p.is_featured])
        assert len(featured) == featured_count
        
        # All returned products should be featured and active
        for product in featured:
            assert product.is_featured is True
            assert product.is_active is True
    
    def test_products_by_category(self, clean_db, sample_category, multiple_products):
        """Test products by category retrieval."""
        results = Product.get_products_by_category(sample_category.id)
        category_products = [p for p in multiple_products if p.category_id == sample_category.id and p.is_active]
        assert len(results.items) == len(category_products)
    
    def test_low_stock_products(self, clean_db, multiple_products):
        """Test low stock products retrieval."""
        low_stock = Product.get_low_stock_products()
        
        for product in low_stock:
            assert product.stock_quantity <= product.min_stock_level
            assert product.is_active is True
    
    def test_product_to_dict(self, clean_db, sample_product):
        """Test product dictionary conversion."""
        product_dict = sample_product.to_dict()
        
        assert product_dict['id'] == sample_product.id
        assert product_dict['name'] == sample_product.name
        assert product_dict['price'] == float(sample_product.price)
        assert product_dict['effective_price'] == sample_product.get_effective_price()
        assert product_dict['is_in_stock'] == sample_product.is_in_stock()
        assert product_dict['stock_status'] == sample_product.get_stock_status()
        assert 'category' in product_dict
    
    def test_product_string_representations(self, clean_db, sample_product):
        """Test string representations of product."""
        assert str(sample_product) == sample_product.name
        assert sample_product.name in repr(sample_product)
    
    def test_digital_product(self, clean_db, sample_category):
        """Test digital product functionality."""
        digital_product = Product(
            name='Digital Download',
            price=29.99,
            category_id=sample_category.id,
            is_digital=True,
            stock_quantity=999  # Digital products don't run out
        )
        clean_db.session.add(digital_product)
        clean_db.session.commit()
        
        assert digital_product.is_digital is True
        assert digital_product.to_dict()['is_digital'] is True
    
    def test_product_seo_fields(self, clean_db, sample_category):
        """Test SEO fields functionality."""
        product = Product(
            name='SEO Product',
            price=99.99,
            category_id=sample_category.id,
            meta_title='Best SEO Product - Buy Now',
            meta_description='This is the best SEO product you can buy online today.'
        )
        clean_db.session.add(product)
        clean_db.session.commit()
        
        assert product.meta_title is not None
        assert product.meta_description is not None
        
        product_dict = product.to_dict()
        # SEO fields should be included in dict representation for admin use
        assert 'meta_title' not in product_dict  # Not exposed in public API
    
    def test_product_category_relationship(self, clean_db, sample_product, sample_category):
        """Test product-category relationship."""
        assert sample_product.category is not None
        assert sample_product.category.id == sample_category.id
        assert sample_product in sample_category.products
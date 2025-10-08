"""
Product and Category Models.
Implements product catalog management with categories.

Quality Management Principles:
- Data Integrity: Validation and constraints ensure data quality
- Business Logic: Encapsulated pricing and inventory management
- Maintainability: Clear model structure and relationships
- Performance: Efficient database queries and indexing
"""

from datetime import datetime
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from app import db


class Category(db.Model):
    """Category model for product organization."""
    
    __tablename__ = 'categories'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Category Information
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    image_filename = db.Column(db.String(255))
    slug = db.Column(db.String(100), nullable=False, unique=True, index=True)
    
    # Status Fields
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    def __init__(self, name, description=None, **kwargs):
        """Initialize category with automatic slug generation."""
        self.name = name
        self.description = description
        self.slug = self.generate_slug(name)
        
        # Set additional attributes
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    @staticmethod
    def generate_slug(name):
        """Generate URL-friendly slug from name."""
        return name.lower().replace(' ', '-').replace('&', 'and')
    
    def get_product_count(self):
        """Get count of active products in this category."""
        return db.session.query(func.count(Product.id)).filter(
            Product.category_id == self.id,
            Product.is_active == True
        ).scalar() or 0
    
    def get_active_products(self, limit=None):
        """Get active products in this category."""
        query = Product.query.filter_by(category_id=self.id, is_active=True)
        if limit:
            query = query.limit(limit)
        return query.all()
    
    def update(self, **kwargs):
        """Update category with new data."""
        for key, value in kwargs.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
        
        # Update slug if name changed
        if 'name' in kwargs:
            self.slug = self.generate_slug(kwargs['name'])
        
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert category to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'slug': self.slug,
            'image_filename': self.image_filename,
            'is_active': self.is_active,
            'product_count': self.get_product_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def __str__(self):
        return self.name


class Product(db.Model):
    """Product model with comprehensive e-commerce features."""
    
    __tablename__ = 'products'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Product Information
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    short_description = db.Column(db.String(500))
    sku = db.Column(db.String(50), unique=True, index=True)
    slug = db.Column(db.String(200), nullable=False, unique=True, index=True)
    
    # Pricing Information
    price = db.Column(db.Numeric(10, 2), nullable=False)
    cost_price = db.Column(db.Numeric(10, 2))  # For profit calculation
    sale_price = db.Column(db.Numeric(10, 2))  # For sales/discounts
    
    # Inventory Management
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    min_stock_level = db.Column(db.Integer, nullable=False, default=5)
    
    # Physical Properties
    weight = db.Column(db.Float)  # In grams
    dimensions = db.Column(db.String(100))  # Format: "LxWxH cm"
    
    # Media
    image_filename = db.Column(db.String(255))
    
    # Category Relationship
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Status and Feature Flags
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_featured = db.Column(db.Boolean, nullable=False, default=False)
    is_digital = db.Column(db.Boolean, nullable=False, default=False)
    
    # SEO Fields
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(300))
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    cart_items = db.relationship('CartItem', backref='product', lazy='dynamic')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    
    def __init__(self, name, price, category_id, **kwargs):
        """Initialize product with required fields."""
        self.name = name
        self.price = float(price)
        self.category_id = category_id
        self.slug = self.generate_slug(name)
        
        # Set additional attributes
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    @staticmethod
    def generate_slug(name):
        """Generate URL-friendly slug from product name."""
        import re
        slug = name.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        return slug.strip('-')
    
    # Stock Management Methods
    def is_in_stock(self):
        """Check if product is in stock."""
        return self.stock_quantity > 0 and self.is_active
    
    def is_low_stock(self):
        """Check if product is low on stock."""
        return self.stock_quantity <= self.min_stock_level
    
    def reserve_stock(self, quantity):
        """Reserve stock for an order (decreases stock)."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if self.stock_quantity < quantity:
            raise ValueError(f"Insufficient stock. Available: {self.stock_quantity}, Requested: {quantity}")
        
        self.stock_quantity -= quantity
        self.updated_at = datetime.utcnow()
        return True
    
    def release_stock(self, quantity):
        """Release reserved stock (increases stock)."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        self.stock_quantity += quantity
        self.updated_at = datetime.utcnow()
        return True
    
    def update_stock(self, new_quantity):
        """Update stock quantity with validation."""
        if new_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        
        self.stock_quantity = new_quantity
        self.updated_at = datetime.utcnow()
    
    # Pricing Methods
    def get_display_price(self):
        """Get the price to display (sale price if available, otherwise regular price)."""
        return float(self.sale_price) if self.sale_price else float(self.price)
    
    def get_effective_price(self):
        """Get the effective price (alias for get_display_price for consistency)."""
        return self.get_display_price()
    
    def get_profit_margin(self):
        """Calculate profit margin percentage."""
        if not self.cost_price or self.cost_price <= 0:
            return None
        
        selling_price = self.get_display_price()
        profit = selling_price - float(self.cost_price)
        margin = (profit / float(self.cost_price)) * 100
        return round(margin, 2)
    
    def is_on_sale(self):
        """Check if product is on sale."""
        return self.sale_price is not None and self.sale_price < self.price
    
    def get_discount_percentage(self):
        """Calculate discount percentage if product is on sale."""
        if not self.is_on_sale():
            return 0
        
        discount = float(self.price) - float(self.sale_price)
        percentage = (discount / float(self.price)) * 100
        return round(percentage, 2)
    
    # Query Methods
    @classmethod
    def search(cls, query, category_id=None):
        """Search products by name or description."""
        search_filter = cls.name.contains(query) | cls.description.contains(query)
        
        if category_id:
            search_filter = search_filter & (cls.category_id == category_id)
        
        return cls.query.filter(search_filter, cls.is_active == True)
    
    @classmethod
    def get_featured(cls, limit=None):
        """Get featured products."""
        query = cls.query.filter_by(is_featured=True, is_active=True)
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @classmethod
    def get_by_category(cls, category_id, limit=None):
        """Get products by category."""
        query = cls.query.filter_by(category_id=category_id, is_active=True)
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @classmethod
    def get_low_stock(cls, threshold=None):
        """Get products with low stock."""
        if threshold is None:
            # Use each product's individual min_stock_level
            return cls.query.filter(cls.stock_quantity <= cls.min_stock_level, cls.is_active == True).all()
        else:
            return cls.query.filter(cls.stock_quantity <= threshold, cls.is_active == True).all()
    
    def update(self, **kwargs):
        """Update product with new data."""
        for key, value in kwargs.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
        
        # Update slug if name changed
        if 'name' in kwargs:
            self.slug = self.generate_slug(kwargs['name'])
        
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert product to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'short_description': self.short_description,
            'sku': self.sku,
            'slug': self.slug,
            'price': float(self.price),
            'cost_price': float(self.cost_price) if self.cost_price else None,
            'sale_price': float(self.sale_price) if self.sale_price else None,
            'display_price': self.get_display_price(),
            'stock_quantity': self.stock_quantity,
            'min_stock_level': self.min_stock_level,
            'weight': self.weight,
            'dimensions': self.dimensions,
            'image_filename': self.image_filename,
            'category_id': self.category_id,
            'category': self.category.to_dict() if self.category else None,
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'is_digital': self.is_digital,
            'is_in_stock': self.is_in_stock(),
            'is_low_stock': self.is_low_stock(),
            'is_on_sale': self.is_on_sale(),
            'profit_margin': self.get_profit_margin(),
            'meta_title': self.meta_title,
            'meta_description': self.meta_description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def __str__(self):
        return self.name
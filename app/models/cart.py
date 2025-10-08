"""
Cart and CartItem Models.
Implements shopping cart functionality for e-commerce.

Quality Management Principles:
- Data Consistency: Proper relationship management
- Performance: Efficient cart operations
- Business Logic: Price calculations and validation
- User Experience: Session-based cart management
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from app import db


class Cart(db.Model):
    """
    Shopping cart model for user sessions.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User (nullable for guest carts)
        session_id (str): Session identifier for guest users
        created_at (datetime): Cart creation timestamp
        updated_at (datetime): Last cart update timestamp
    """
    
    __tablename__ = 'carts'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # User Relationship (nullable for guest carts)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, unique=True)
    
    # Session Management for Guest Users
    session_id = db.Column(db.String(255), nullable=True, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, user_id=None, session_id=None):
        """Initialize cart for user or session."""
        self.user_id = user_id
        self.session_id = session_id
    
    def add_item(self, product_id, quantity=1):
        """
        Add item to cart or update quantity if exists.
        
        Args:
            product_id (int): Product ID to add
            quantity (int): Quantity to add
            
        Returns:
            CartItem: The cart item that was added or updated
        """
        from app.models.product import Product
        
        # Validate product exists and is active
        product = Product.query.filter_by(id=product_id, is_active=True).first()
        if not product:
            raise ValueError("Product not found or inactive")
        
        # Check stock availability
        existing_item = self.get_item_by_product(product_id)
        total_quantity = quantity + (existing_item.quantity if existing_item else 0)
        
        if total_quantity > product.stock_quantity:
            raise ValueError(f"Insufficient stock. Available: {product.stock_quantity}")
        
        # Add or update item
        if existing_item:
            existing_item.quantity += quantity
            existing_item.updated_at = datetime.utcnow()
            cart_item = existing_item
        else:
            cart_item = CartItem(
                cart_id=self.id,
                product_id=product_id,
                quantity=quantity,
                price=product.get_effective_price()
            )
            db.session.add(cart_item)
        
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return cart_item
    
    def update_item_quantity(self, product_id, quantity):
        """
        Update item quantity in cart.
        
        Args:
            product_id (int): Product ID to update
            quantity (int): New quantity (0 to remove)
        """
        from app.models.product import Product
        
        cart_item = self.get_item_by_product(product_id)
        if not cart_item:
            raise ValueError("Item not found in cart")
        
        if quantity <= 0:
            self.remove_item(product_id)
            return
        
        # Check stock availability
        product = Product.query.get(product_id)
        if quantity > product.stock_quantity:
            raise ValueError(f"Insufficient stock. Available: {product.stock_quantity}")
        
        cart_item.quantity = quantity
        cart_item.updated_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def remove_item(self, product_id):
        """Remove item from cart."""
        cart_item = self.get_item_by_product(product_id)
        if cart_item:
            db.session.delete(cart_item)
            self.updated_at = datetime.utcnow()
            db.session.commit()
    
    def clear_cart(self):
        """Remove all items from cart."""
        for item in self.items:
            db.session.delete(item)
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def get_item_by_product(self, product_id):
        """Get cart item by product ID."""
        return next((item for item in self.items if item.product_id == product_id), None)
    
    def get_total_items(self):
        """Get total number of items in cart."""
        return sum(item.quantity for item in self.items)
    
    def get_total_amount(self):
        """Get total cart amount."""
        return sum(item.get_total_price() for item in self.items)
    
    def get_item_count(self):
        """Get number of unique items in cart."""
        return len(self.items)
    
    def is_empty(self):
        """Check if cart is empty."""
        return len(self.items) == 0
    
    def validate_stock_availability(self):
        """
        Validate that all cart items are available in stock.
        
        Returns:
            list: List of items with insufficient stock
        """
        unavailable_items = []
        for item in self.items:
            if not item.product.is_active:
                unavailable_items.append({
                    'item': item,
                    'issue': 'Product is no longer available'
                })
            elif item.quantity > item.product.stock_quantity:
                unavailable_items.append({
                    'item': item,
                    'issue': f'Only {item.product.stock_quantity} items available'
                })
        return unavailable_items
    
    def to_dict(self):
        """Convert cart to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'total_items': self.get_total_items(),
            'total_amount': float(self.get_total_amount()),
            'item_count': self.get_item_count(),
            'is_empty': self.is_empty(),
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Cart {self.id} - {self.get_total_items()} items>'


class CartItem(db.Model):
    """
    Individual cart item model.
    
    Attributes:
        id (int): Primary key
        cart_id (int): Foreign key to Cart
        product_id (int): Foreign key to Product
        quantity (int): Item quantity
        price (float): Price at time of adding to cart
        created_at (datetime): Item creation timestamp
        updated_at (datetime): Last item update timestamp
    """
    
    __tablename__ = 'cart_items'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Relationships
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Item Details
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Price at time of adding
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint to prevent duplicate items
    __table_args__ = (db.UniqueConstraint('cart_id', 'product_id', name='unique_cart_product'),)
    
    def __init__(self, cart_id, product_id, quantity, price):
        """Initialize cart item."""
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
    
    def get_total_price(self):
        """Get total price for this cart item."""
        return float(self.price) * self.quantity
    
    def update_price(self):
        """Update price to current product price."""
        if self.product:
            self.price = self.product.get_effective_price()
            self.updated_at = datetime.utcnow()
            db.session.commit()
    
    def to_dict(self):
        """Convert cart item to dictionary."""
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'price': float(self.price),
            'total_price': self.get_total_price(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<CartItem {self.id} - {self.quantity}x {self.product.name if self.product else "Product"}>'
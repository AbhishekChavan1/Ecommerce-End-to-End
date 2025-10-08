"""
Order and OrderItem Models.
Implements order management and tracking for e-commerce.

Quality Management Principles:
- Data Integrity: Complete order tracking and audit trails
- Business Logic: Order status workflow and validation
- Financial Accuracy: Precise pricing and totals calculation
- Traceability: Complete order history and status changes
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from app import db


class OrderStatus(Enum):
    """Order status enumeration."""
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    RETURNED = 'returned'


class PaymentStatus(Enum):
    """Payment status enumeration."""
    PENDING = 'pending'
    PAID = 'paid'
    FAILED = 'failed'
    REFUNDED = 'refunded'
    PARTIALLY_REFUNDED = 'partially_refunded'


class Order(db.Model):
    """
    Order model for managing customer orders.
    
    Attributes:
        id (int): Primary key
        order_number (str): Unique order identifier
        user_id (int): Foreign key to User
        status (str): Order status
        payment_status (str): Payment status
        total_amount (float): Total order amount
        tax_amount (float): Tax amount
        shipping_amount (float): Shipping cost
        discount_amount (float): Discount applied
        payment_method (str): Payment method used
        shipping_address (dict): Shipping address details
        billing_address (dict): Billing address details
        notes (str): Order notes
        created_at (datetime): Order creation timestamp
        updated_at (datetime): Last order update timestamp
        shipped_at (datetime): Shipping timestamp
        delivered_at (datetime): Delivery timestamp
    """
    
    __tablename__ = 'orders'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Order Identification
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # User Relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Order Status
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    payment_status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    
    # Financial Information
    subtotal_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    tax_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    shipping_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    discount_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Payment Information
    payment_method = db.Column(db.String(50), nullable=True)
    payment_reference = db.Column(db.String(255), nullable=True)
    
    # Address Information (stored as JSON)
    shipping_address = db.Column(db.JSON, nullable=False)
    billing_address = db.Column(db.JSON, nullable=True)
    
    # Additional Information
    notes = db.Column(db.Text, nullable=True)
    tracking_number = db.Column(db.String(100), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    shipped_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, user_id, shipping_address, **kwargs):
        """Initialize order with required fields."""
        self.user_id = user_id
        self.shipping_address = shipping_address
        self.order_number = self.generate_order_number()
        
        # Set default values for amount fields
        self.subtotal_amount = kwargs.get('subtotal_amount', 0)
        self.tax_amount = kwargs.get('tax_amount', 0)
        self.shipping_amount = kwargs.get('shipping_amount', 0)
        self.discount_amount = kwargs.get('discount_amount', 0)
        self.total_amount = kwargs.get('total_amount', 0)
        
        # Set other attributes
        for key, value in kwargs.items():
            if key not in ['subtotal_amount', 'tax_amount', 'shipping_amount', 'discount_amount', 'total_amount']:
                setattr(self, key, value)
    
    @staticmethod
    def generate_order_number():
        """Generate unique order number."""
        from datetime import datetime
        import random
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        random_suffix = str(random.randint(100, 999))
        return f"ORD-{timestamp}-{random_suffix}"
    
    def add_item_from_cart_item(self, cart_item):
        """
        Add order item from cart item.
        
        Args:
            cart_item: CartItem instance to convert to OrderItem
        """
        order_item = OrderItem(
            order_id=self.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.price
        )
        db.session.add(order_item)
        return order_item
    
    def calculate_totals(self):
        """Calculate and update order totals."""
        self.subtotal_amount = sum(item.get_total_price() for item in self.items)
        self.tax_amount = self.calculate_tax()
        # shipping_amount and discount_amount should be set separately
        self.total_amount = (
            self.subtotal_amount + 
            self.tax_amount + 
            self.shipping_amount - 
            self.discount_amount
        )
        self.updated_at = datetime.utcnow()
    
    def calculate_tax(self, tax_rate=0.08):
        """Calculate tax amount based on subtotal."""
        return self.subtotal_amount * tax_rate
    
    def update_status(self, new_status, notes=None):
        """
        Update order status with validation and logging.
        
        Args:
            new_status (OrderStatus): New status to set
            notes (str): Optional notes about status change
        """
        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.utcnow()
        
        # Set specific timestamps based on status
        if new_status == OrderStatus.CONFIRMED:
            self.confirmed_at = datetime.utcnow()
        elif new_status == OrderStatus.SHIPPED:
            self.shipped_at = datetime.utcnow()
        elif new_status == OrderStatus.DELIVERED:
            self.delivered_at = datetime.utcnow()
        
        if notes:
            self.notes = f"{self.notes or ''}\n{datetime.utcnow()}: Status changed from {old_status.value} to {new_status.value}. {notes}".strip()
        
        db.session.commit()
    
    def update_payment_status(self, new_status, reference=None):
        """Update payment status."""
        self.payment_status = new_status
        if reference:
            self.payment_reference = reference
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def can_be_cancelled(self):
        """Check if order can be cancelled."""
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]
    
    def can_be_shipped(self):
        """Check if order can be shipped."""
        return self.status == OrderStatus.CONFIRMED and self.payment_status == PaymentStatus.PAID
    
    def get_total_items(self):
        """Get total number of items in order."""
        return sum(item.quantity for item in self.items)
    
    def get_item_count(self):
        """Get number of unique items in order."""
        return len(self.items)
    
    def reserve_stock(self):
        """Reserve stock for all order items."""
        for item in self.items:
            item.product.reserve_stock(item.quantity)
    
    def release_stock(self):
        """Release reserved stock (e.g., when order is cancelled)."""
        for item in self.items:
            item.product.release_stock(item.quantity)
    
    def get_status_history(self):
        """Parse notes to get status change history."""
        if not self.notes:
            return []
        
        history = []
        for line in self.notes.split('\n'):
            if 'Status changed' in line:
                history.append(line.strip())
        return history
    
    def to_dict(self):
        """Convert order to dictionary."""
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'status': self.status.value,
            'payment_status': self.payment_status.value,
            'subtotal_amount': float(self.subtotal_amount),
            'tax_amount': float(self.tax_amount),
            'shipping_amount': float(self.shipping_amount),
            'discount_amount': float(self.discount_amount),
            'total_amount': float(self.total_amount),
            'payment_method': self.payment_method,
            'payment_reference': self.payment_reference,
            'shipping_address': self.shipping_address,
            'billing_address': self.billing_address,
            'tracking_number': self.tracking_number,
            'notes': self.notes,
            'total_items': self.get_total_items(),
            'item_count': self.get_item_count(),
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None,
            'shipped_at': self.shipped_at.isoformat() if self.shipped_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None
        }
    
    def __repr__(self):
        return f'<Order {self.order_number} - {self.status.value}>'
    
    # Class methods for order management
    @classmethod
    def create_from_cart(cls, user, cart, shipping_address, payment_method='credit_card', **kwargs):
        """
        Create order from user's cart.
        
        Args:
            user: User instance
            cart: Cart instance
            shipping_address: Shipping address dictionary
            payment_method: Payment method string
            
        Returns:
            Order: Created order instance
        """
        if cart.is_empty():
            raise ValueError("Cannot create order from empty cart")
        
        # Validate stock availability
        unavailable_items = cart.validate_stock_availability()
        if unavailable_items:
            raise ValueError(f"Some items are not available: {unavailable_items}")
        
        # Create order
        order = cls(
            user_id=user.id,
            shipping_address=shipping_address,
            billing_address=kwargs.get('billing_address', shipping_address),
            payment_method=payment_method,
            **kwargs
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Add order items from cart
        for cart_item in cart.items:
            order.add_item_from_cart_item(cart_item)
        
        # Calculate totals
        order.calculate_totals()
        
        # Reserve stock
        order.reserve_stock()
        
        db.session.commit()
        return order


class OrderItem(db.Model):
    """
    Individual order item model.
    
    Attributes:
        id (int): Primary key
        order_id (int): Foreign key to Order
        product_id (int): Foreign key to Product
        quantity (int): Item quantity
        price (float): Price at time of order
        created_at (datetime): Item creation timestamp
    """
    
    __tablename__ = 'order_items'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Relationships
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Item Details
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Price at time of order
    
    # Product snapshot (in case product details change)
    product_name = db.Column(db.String(200), nullable=False)
    product_sku = db.Column(db.String(50), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __init__(self, order_id, product_id, quantity, price):
        """Initialize order item."""
        from app.models.product import Product
        
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        
        # Store product snapshot
        product = Product.query.get(product_id)
        if product:
            self.product_name = product.name
            self.product_sku = product.sku
    
    def get_total_price(self):
        """Get total price for this order item."""
        return float(self.price) * self.quantity
    
    def to_dict(self):
        """Convert order item to dictionary."""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_sku': self.product_sku,
            'quantity': self.quantity,
            'price': float(self.price),
            'total_price': self.get_total_price(),
            'product': self.product.to_dict() if self.product else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<OrderItem {self.id} - {self.quantity}x {self.product_name}>'
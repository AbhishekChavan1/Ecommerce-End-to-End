"""
User Model.
Implements user authentication and profile management.

Quality Management Principles:
- Data Integrity: Proper validation and constraints
- Security: Password hashing with bcrypt
- Separation of Concerns: User-specific business logic encapsulated
- Extensibility: Support for admin and regular users
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """
    User model for authentication and profile management.
    
    Attributes:
        id (int): Primary key
        username (str): Unique username for login
        email (str): Unique email address
        password_hash (str): Hashed password for security
        first_name (str): User's first name
        last_name (str): User's last name
        is_admin (bool): Admin privileges flag
        is_active (bool): Account active status
        created_at (datetime): Account creation timestamp
        updated_at (datetime): Last profile update timestamp
    """
    
    __tablename__ = 'users'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Authentication Fields
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Profile Fields
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    
    # Address Fields
    address_line1 = db.Column(db.String(100), nullable=True)
    address_line2 = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(50), nullable=True, default='United States')
    
    # Account Status
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    cart = db.relationship('Cart', backref='user', uselist=False, lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, username, email, first_name, last_name, **kwargs):
        """Initialize user with required fields."""
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def get_address(self):
        """Get formatted address string."""
        address_parts = [
            self.address_line1,
            self.address_line2,
            f"{self.city}, {self.state} {self.postal_code}",
            self.country
        ]
        return '\n'.join(filter(None, address_parts))
    
    def has_complete_profile(self):
        """Check if user has completed their profile."""
        required_fields = [
            self.first_name, self.last_name, self.phone,
            self.address_line1, self.city, self.state, self.postal_code
        ]
        return all(field is not None and field.strip() for field in required_fields)
    
    def update_last_login(self):
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convert user to dictionary (excluding sensitive data)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'phone': self.phone,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'email_confirmed': self.email_confirmed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'has_complete_profile': self.has_complete_profile()
        }
    
    def __repr__(self):
        """String representation of user."""
        return f'<User {self.username}>'
    
    def __str__(self):
        """Human-readable string representation."""
        return f"{self.get_full_name()} ({self.username})"
    
    # Flask-Login required methods
    def get_id(self):
        """Get user ID as string for Flask-Login."""
        return str(self.id)
    
    @property
    def is_authenticated(self):
        """Check if user is authenticated."""
        return True
    
    @property
    def is_anonymous(self):
        """Check if user is anonymous."""
        return False
    
    # Class methods for user management
    @classmethod
    def create_user(cls, username, email, password, first_name, last_name, **kwargs):
        """Create a new user with validation."""
        # Check if username or email already exists
        if cls.query.filter_by(username=username).first():
            raise ValueError(f"Username '{username}' already exists")
        
        if cls.query.filter_by(email=email).first():
            raise ValueError(f"Email '{email}' already exists")
        
        # Create new user
        user = cls(username=username, email=email, first_name=first_name, last_name=last_name, **kwargs)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @classmethod
    def authenticate(cls, username_or_email, password):
        """Authenticate user by username/email and password."""
        user = cls.query.filter(
            (cls.username == username_or_email) | (cls.email == username_or_email)
        ).first()
        
        if user and user.check_password(password) and user.is_active:
            user.update_last_login()
            return user
        
        return None
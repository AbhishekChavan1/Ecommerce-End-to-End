"""
Shop Forms.
Implements forms for shopping cart and checkout functionality.

Quality Management Principles:
- Input Validation: Proper quantity and address validation
- Security: CSRF protection and data sanitization
- User Experience: Clear form structure and validation messages
- Data Integrity: Address and payment information validation
"""

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange, Length, Email, Regexp, Optional


class AddToCartForm(FlaskForm):
    """Form for adding products to cart."""
    
    product_id = HiddenField(
        'Product ID',
        validators=[DataRequired()]
    )
    
    quantity = IntegerField(
        'Quantity',
        validators=[
            DataRequired(message='Quantity is required'),
            NumberRange(min=1, max=100, message='Quantity must be between 1 and 100')
        ],
        default=1,
        render_kw={
            'class': 'form-control quantity-input',
            'min': '1',
            'max': '100'
        }
    )
    
    submit = SubmitField(
        'Add to Cart',
        render_kw={'class': 'btn btn-primary btn-add-to-cart'}
    )


class UpdateCartForm(FlaskForm):
    """Form for updating cart item quantities."""
    
    item_id = HiddenField(
        'Item ID',
        validators=[DataRequired()]
    )
    
    quantity = IntegerField(
        'Quantity',
        validators=[
            DataRequired(message='Quantity is required'),
            NumberRange(min=0, max=100, message='Quantity must be between 0 and 100')
        ],
        render_kw={
            'class': 'form-control quantity-input',
            'min': '0',
            'max': '100'
        }
    )
    
    submit = SubmitField(
        'Update',
        render_kw={'class': 'btn btn-sm btn-outline-primary'}
    )


class CheckoutForm(FlaskForm):
    """Form for checkout process."""
    
    # Shipping Information
    shipping_first_name = StringField(
        'First Name',
        validators=[
            DataRequired(message='First name is required'),
            Length(min=1, max=50, message='First name must be between 1 and 50 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter first name'
        }
    )
    
    shipping_last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(message='Last name is required'),
            Length(min=1, max=50, message='Last name must be between 1 and 50 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter last name'
        }
    )
    
    shipping_email = StringField(
        'Email Address',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Please enter a valid email address')
        ],
        render_kw={
            'class': 'form-control',
            'type': 'email',
            'placeholder': 'Enter email address'
        }
    )
    
    shipping_phone = StringField(
        'Phone Number',
        validators=[
            DataRequired(message='Phone number is required'),
            Length(max=20, message='Phone number must be less than 20 characters'),
            Regexp(
                r'^[\d\s\+\-\(\)\.]+$',
                message='Please enter a valid phone number'
            )
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '+1 (555) 123-4567'
        }
    )
    
    shipping_address_line1 = StringField(
        'Address Line 1',
        validators=[
            DataRequired(message='Address is required'),
            Length(max=100, message='Address must be less than 100 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '123 Main Street'
        }
    )
    
    shipping_address_line2 = StringField(
        'Address Line 2',
        validators=[
            Length(max=100, message='Address line 2 must be less than 100 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Apt 4B (optional)'
        }
    )
    
    shipping_city = StringField(
        'City',
        validators=[
            DataRequired(message='City is required'),
            Length(max=50, message='City must be less than 50 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'New York'
        }
    )
    
    shipping_state = StringField(
        'State/Province',
        validators=[
            DataRequired(message='State is required'),
            Length(max=50, message='State must be less than 50 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'NY'
        }
    )
    
    shipping_postal_code = StringField(
        'Postal Code',
        validators=[
            DataRequired(message='Postal code is required'),
            Length(max=20, message='Postal code must be less than 20 characters'),
            Regexp(
                r'^[\d\w\s\-]+$',
                message='Please enter a valid postal code'
            )
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '10001'
        }
    )
    
    shipping_country = StringField(
        'Country',
        validators=[
            DataRequired(message='Country is required'),
            Length(max=50, message='Country must be less than 50 characters')
        ],
        default='United States',
        render_kw={
            'class': 'form-control',
            'placeholder': 'United States'
        }
    )
    
    # Payment Information
    payment_method = SelectField(
        'Payment Method',
        validators=[DataRequired(message='Please select a payment method')],
        choices=[
            ('credit_card', 'Credit Card'),
            ('debit_card', 'Debit Card'),
            ('paypal', 'PayPal'),
            ('bank_transfer', 'Bank Transfer')
        ],
        render_kw={'class': 'form-control'}
    )
    
    # Order Notes
    notes = TextAreaField(
        'Order Notes',
        validators=[
            Length(max=500, message='Notes must be less than 500 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Special instructions for your order (optional)'
        }
    )
    
    submit = SubmitField(
        'Place Order',
        render_kw={'class': 'btn btn-success btn-lg btn-block'}
    )


class SearchForm(FlaskForm):
    """Form for product search."""
    
    query = StringField(
        'Search Products',
        validators=[
            Length(max=100, message='Search query must be less than 100 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Search for products...',
            'id': 'search-input'
        }
    )
    
    category = SelectField(
        'Category',
        coerce=int,
        render_kw={'class': 'form-control'}
    )
    
    sort_by = SelectField(
        'Sort By',
        choices=[
            ('name_asc', 'Name (A-Z)'),
            ('name_desc', 'Name (Z-A)'),
            ('price_asc', 'Price (Low to High)'),
            ('price_desc', 'Price (High to Low)'),
            ('newest', 'Newest First'),
            ('oldest', 'Oldest First')
        ],
        default='name_asc',
        render_kw={'class': 'form-control'}
    )
    
    submit = SubmitField(
        'Search',
        render_kw={'class': 'btn btn-primary'}
    )
    
    def __init__(self, *args, **kwargs):
        """Initialize form with category choices."""
        super(SearchForm, self).__init__(*args, **kwargs)
        from app.models.product import Category
        self.category.choices = [(0, 'All Categories')] + [
            (category.id, category.name) 
            for category in Category.query.filter_by(is_active=True).order_by(Category.name).all()
        ]
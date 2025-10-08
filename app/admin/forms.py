"""
Admin Forms.
Implements forms for admin product and category management.

Quality Management Principles:
- Input Validation: Comprehensive validation for product data
- File Upload Security: Safe image upload handling
- Data Integrity: Price and inventory validation
- User Experience: Clear form structure and error handling
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError, Optional
from decimal import Decimal
from app.models.product import Category, Product


class CategoryForm(FlaskForm):
    """Form for creating and editing categories."""
    
    name = StringField(
        'Category Name',
        validators=[
            DataRequired(message='Category name is required'),
            Length(min=1, max=100, message='Category name must be between 1 and 100 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter category name'
        }
    )
    
    description = TextAreaField(
        'Description',
        validators=[
            Length(max=500, message='Description must be less than 500 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter category description (optional)'
        }
    )
    
    image = FileField(
        'Category Image',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
        ],
        render_kw={'class': 'form-control-file'}
    )
    
    is_active = BooleanField(
        'Active',
        default=True,
        render_kw={'class': 'form-check-input'}
    )
    
    submit = SubmitField(
        'Save Category',
        render_kw={'class': 'btn btn-primary'}
    )
    
    def validate_name(self, name):
        """Validate category name uniqueness."""
        category = Category.query.filter_by(name=name.data).first()
        if category and (not hasattr(self, 'category_id') or category.id != self.category_id):
            raise ValidationError('Category name already exists.')


class ProductForm(FlaskForm):
    """Form for creating and editing products."""
    
    name = StringField(
        'Product Name',
        validators=[
            DataRequired(message='Product name is required'),
            Length(min=1, max=200, message='Product name must be between 1 and 200 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter product name'
        }
    )
    
    short_description = TextAreaField(
        'Short Description',
        validators=[
            Length(max=500, message='Short description must be less than 500 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Brief product description for listings'
        }
    )
    
    description = TextAreaField(
        'Full Description',
        validators=[
            Length(max=2000, message='Description must be less than 2000 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Detailed product description'
        }
    )
    
    sku = StringField(
        'SKU (Stock Keeping Unit)',
        validators=[
            Length(max=50, message='SKU must be less than 50 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'e.g., LAPTOP-001 (optional)'
        }
    )
    
    category_id = SelectField(
        'Category',
        validators=[DataRequired(message='Please select a category')],
        coerce=int,
        render_kw={'class': 'form-control'}
    )
    
    price = FloatField(
        'Price ($)',
        validators=[
            DataRequired(message='Price is required'),
            NumberRange(min=0.01, message='Price must be greater than $0.00')
        ],
        render_kw={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '0.00'
        }
    )
    
    cost_price = FloatField(
        'Cost Price ($)',
        validators=[
            Optional(),
            NumberRange(min=0, message='Cost price cannot be negative')
        ],
        render_kw={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '0.00 (optional)'
        }
    )
    
    sale_price = FloatField(
        'Sale Price ($)',
        validators=[
            Optional(),
            NumberRange(min=0.01, message='Sale price must be greater than $0.00')
        ],
        render_kw={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '0.00 (optional - for discounts)'
        }
    )
    
    stock_quantity = IntegerField(
        'Stock Quantity',
        validators=[
            DataRequired(message='Stock quantity is required'),
            NumberRange(min=0, message='Stock quantity cannot be negative')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '0'
        }
    )
    
    min_stock_level = IntegerField(
        'Minimum Stock Level',
        validators=[
            DataRequired(message='Minimum stock level is required'),
            NumberRange(min=0, message='Minimum stock level cannot be negative')
        ],
        default=5,
        render_kw={
            'class': 'form-control',
            'placeholder': '5'
        }
    )
    
    weight = FloatField(
        'Weight (kg)',
        validators=[
            Optional(),
            NumberRange(min=0, message='Weight cannot be negative')
        ],
        render_kw={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '0.00 (optional)'
        }
    )
    
    dimensions = StringField(
        'Dimensions (L x W x H)',
        validators=[
            Length(max=100, message='Dimensions must be less than 100 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'e.g., 30 x 20 x 5 cm (optional)'
        }
    )
    
    image = FileField(
        'Product Image',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
        ],
        render_kw={'class': 'form-control-file'}
    )
    
    is_active = BooleanField(
        'Active',
        default=True,
        render_kw={'class': 'form-check-input'}
    )
    
    is_featured = BooleanField(
        'Featured Product',
        default=False,
        render_kw={'class': 'form-check-input'}
    )
    
    is_digital = BooleanField(
        'Digital Product',
        default=False,
        render_kw={'class': 'form-check-input'}
    )
    
    meta_title = StringField(
        'SEO Title',
        validators=[
            Length(max=200, message='SEO title must be less than 200 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'SEO-friendly title (optional)'
        }
    )
    
    meta_description = TextAreaField(
        'SEO Description',
        validators=[
            Length(max=300, message='SEO description must be less than 300 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'SEO meta description (optional)'
        }
    )
    
    submit = SubmitField(
        'Save Product',
        render_kw={'class': 'btn btn-primary'}
    )
    
    def __init__(self, *args, **kwargs):
        """Initialize form with category choices."""
        super(ProductForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [
            (category.id, category.name) 
            for category in Category.query.filter_by(is_active=True).order_by(Category.name).all()
        ]
        if not self.category_id.choices:
            self.category_id.choices = [(0, 'No categories available')]
    
    def validate_sku(self, sku):
        """Validate SKU uniqueness if provided."""
        if sku.data:
            product = Product.query.filter_by(sku=sku.data).first()
            if product and (not hasattr(self, 'product_id') or product.id != self.product_id):
                raise ValidationError('SKU already exists.')
    
    def validate_sale_price(self, sale_price):
        """Validate that sale price is less than regular price."""
        if sale_price.data and self.price.data:
            if sale_price.data >= self.price.data:
                raise ValidationError('Sale price must be less than regular price.')


class BulkUpdateForm(FlaskForm):
    """Form for bulk updating products."""
    
    action = SelectField(
        'Action',
        validators=[DataRequired()],
        choices=[
            ('', 'Select action...'),
            ('activate', 'Activate Products'),
            ('deactivate', 'Deactivate Products'),
            ('feature', 'Mark as Featured'),
            ('unfeature', 'Remove from Featured'),
            ('delete', 'Delete Products')
        ],
        render_kw={'class': 'form-control'}
    )
    
    submit = SubmitField(
        'Apply to Selected',
        render_kw={'class': 'btn btn-warning'}
    )
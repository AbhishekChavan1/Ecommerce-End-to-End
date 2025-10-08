"""
Authentication Forms.
Implements WTForms for secure form handling and validation.

Quality Management Principles:
- Input Validation: Comprehensive field validation
- Security: CSRF protection and secure password handling
- User Experience: Clear error messages and field validation
- Data Integrity: Email and username uniqueness validation
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
from app.models.user import User


class LoginForm(FlaskForm):
    """User login form with validation."""
    
    username_or_email = StringField(
        'Username or Email',
        validators=[
            DataRequired(message='Username or email is required'),
            Length(min=3, max=120, message='Username or email must be between 3 and 120 characters')
        ],
        render_kw={
            'placeholder': 'Enter username or email',
            'class': 'form-control',
            'id': 'username_or_email'
        }
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required'),
            Length(min=6, message='Password must be at least 6 characters long')
        ],
        render_kw={
            'placeholder': 'Enter password',
            'class': 'form-control',
            'id': 'password'
        }
    )
    
    remember_me = BooleanField(
        'Remember Me',
        render_kw={'class': 'form-check-input'}
    )
    
    submit = SubmitField(
        'Sign In',
        render_kw={'class': 'btn btn-primary btn-block'}
    )


class RegistrationForm(FlaskForm):
    """User registration form with comprehensive validation."""
    
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=80, message='Username must be between 3 and 80 characters'),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message='Username can only contain letters, numbers, and underscores'
            )
        ],
        render_kw={
            'placeholder': 'Choose a username',
            'class': 'form-control',
            'id': 'username'
        }
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Please enter a valid email address'),
            Length(max=120, message='Email must be less than 120 characters')
        ],
        render_kw={
            'placeholder': 'Enter your email address',
            'class': 'form-control',
            'type': 'email',
            'id': 'email'
        }
    )
    
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(message='First name is required'),
            Length(min=1, max=50, message='First name must be between 1 and 50 characters'),
            Regexp(
                r'^[a-zA-Z\s]+$',
                message='First name can only contain letters and spaces'
            )
        ],
        render_kw={
            'placeholder': 'Enter your first name',
            'class': 'form-control',
            'id': 'first_name'
        }
    )
    
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(message='Last name is required'),
            Length(min=1, max=50, message='Last name must be between 1 and 50 characters'),
            Regexp(
                r'^[a-zA-Z\s]+$',
                message='Last name can only contain letters and spaces'
            )
        ],
        render_kw={
            'placeholder': 'Enter your last name',
            'class': 'form-control',
            'id': 'last_name'
        }
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required'),
            Length(min=8, message='Password must be at least 8 characters long'),
            Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
                message='Password must contain at least one lowercase letter, one uppercase letter, and one number'
            )
        ],
        render_kw={
            'placeholder': 'Create a strong password',
            'class': 'form-control',
            'id': 'password'
        }
    )
    
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message='Please confirm your password'),
            EqualTo('password', message='Passwords must match')
        ],
        render_kw={
            'placeholder': 'Confirm your password',
            'class': 'form-control',
            'id': 'confirm_password'
        }
    )
    
    submit = SubmitField(
        'Create Account',
        render_kw={'class': 'btn btn-primary btn-block'}
    )
    
    def validate_username(self, username):
        """Custom validation to check username uniqueness."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        """Custom validation to check email uniqueness."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email or sign in.')


class ProfileForm(FlaskForm):
    """User profile update form."""
    
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(message='First name is required'),
            Length(min=1, max=50, message='First name must be between 1 and 50 characters')
        ],
        render_kw={
            'class': 'form-control',
            'id': 'first_name'
        }
    )
    
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(message='Last name is required'),
            Length(min=1, max=50, message='Last name must be between 1 and 50 characters')
        ],
        render_kw={
            'class': 'form-control',
            'id': 'last_name'
        }
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Please enter a valid email address')
        ],
        render_kw={
            'class': 'form-control',
            'type': 'email',
            'id': 'email'
        }
    )
    
    phone = StringField(
        'Phone Number',
        validators=[
            Length(max=20, message='Phone number must be less than 20 characters'),
            Regexp(
                r'^[\d\s\+\-\(\)\.]+$',
                message='Please enter a valid phone number'
            )
        ],
        render_kw={
            'placeholder': '+1 (555) 123-4567',
            'class': 'form-control',
            'id': 'phone'
        }
    )
    
    address_line1 = StringField(
        'Address Line 1',
        validators=[
            Length(max=100, message='Address line 1 must be less than 100 characters')
        ],
        render_kw={
            'placeholder': '123 Main Street',
            'class': 'form-control',
            'id': 'address_line1'
        }
    )
    
    address_line2 = StringField(
        'Address Line 2',
        validators=[
            Length(max=100, message='Address line 2 must be less than 100 characters')
        ],
        render_kw={
            'placeholder': 'Apt 4B (optional)',
            'class': 'form-control',
            'id': 'address_line2'
        }
    )
    
    city = StringField(
        'City',
        validators=[
            Length(max=50, message='City must be less than 50 characters')
        ],
        render_kw={
            'placeholder': 'New York',
            'class': 'form-control',
            'id': 'city'
        }
    )
    
    state = StringField(
        'State/Province',
        validators=[
            Length(max=50, message='State must be less than 50 characters')
        ],
        render_kw={
            'placeholder': 'NY',
            'class': 'form-control',
            'id': 'state'
        }
    )
    
    postal_code = StringField(
        'Postal Code',
        validators=[
            Length(max=20, message='Postal code must be less than 20 characters'),
            Regexp(
                r'^[\d\w\s\-]+$',
                message='Please enter a valid postal code'
            )
        ],
        render_kw={
            'placeholder': '10001',
            'class': 'form-control',
            'id': 'postal_code'
        }
    )
    
    country = StringField(
        'Country',
        validators=[
            Length(max=50, message='Country must be less than 50 characters')
        ],
        render_kw={
            'placeholder': 'United States',
            'class': 'form-control',
            'id': 'country'
        }
    )
    
    submit = SubmitField(
        'Update Profile',
        render_kw={'class': 'btn btn-primary'}
    )


class ChangePasswordForm(FlaskForm):
    """Password change form for authenticated users."""
    
    current_password = PasswordField(
        'Current Password',
        validators=[
            DataRequired(message='Current password is required')
        ],
        render_kw={
            'class': 'form-control',
            'id': 'current_password'
        }
    )
    
    new_password = PasswordField(
        'New Password',
        validators=[
            DataRequired(message='New password is required'),
            Length(min=8, message='Password must be at least 8 characters long'),
            Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
                message='Password must contain at least one lowercase letter, one uppercase letter, and one number'
            )
        ],
        render_kw={
            'class': 'form-control',
            'id': 'new_password'
        }
    )
    
    confirm_new_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(message='Please confirm your new password'),
            EqualTo('new_password', message='Passwords must match')
        ],
        render_kw={
            'class': 'form-control',
            'id': 'confirm_new_password'
        }
    )
    
    submit = SubmitField(
        'Change Password',
        render_kw={'class': 'btn btn-primary'}
    )
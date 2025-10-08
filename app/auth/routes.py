"""
Authentication Routes.
Implements user authentication endpoints with security best practices.

Quality Management Principles:
- Security: Proper session management and CSRF protection
- Error Handling: Comprehensive error handling and user feedback
- Logging: Audit trail for authentication events
- User Experience: Clear messages and proper redirects
"""

from flask import render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.models.cart import Cart
from . import auth_bp
from .forms import LoginForm, RegistrationForm, ProfileForm, ChangePasswordForm


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login endpoint.
    Handles user authentication and session management.
    """
    # Redirect if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('shop.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username_or_email = form.username_or_email.data.lower().strip()
        password = form.password.data
        remember = form.remember_me.data
        
        # Authenticate user
        user = User.authenticate(username_or_email, password)
        
        if user:
            # Log successful login
            current_app.logger.info(f'Successful login for user: {user.username}')
            
            # Login user with Flask-Login
            login_user(user, remember=remember)
            
            # Merge guest cart with user cart if exists
            merge_guest_cart_with_user_cart(user)
            
            # Redirect to intended page or shop
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('shop.index')
            
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(next_page)
        
        else:
            # Log failed login attempt
            current_app.logger.warning(f'Failed login attempt for: {username_or_email}')
            flash('Invalid username/email or password. Please try again.', 'error')
    
    return render_template('auth/login.html', form=form, title='Sign In')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration endpoint.
    Creates new user account with validation.
    """
    # Redirect if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('shop.index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            # Create new user
            user = User.create_user(
                username=form.username.data.lower().strip(),
                email=form.email.data.lower().strip(),
                password=form.password.data,
                first_name=form.first_name.data.strip(),
                last_name=form.last_name.data.strip()
            )
            
            # Log successful registration
            current_app.logger.info(f'New user registered: {user.username}')
            
            # Create user cart
            cart = Cart(user_id=user.id)
            db.session.add(cart)
            db.session.commit()
            
            # Login the new user
            login_user(user)
            
            flash(f'Registration successful! Welcome to our store, {user.first_name}!', 'success')
            return redirect(url_for('shop.index'))
        
        except ValueError as e:
            # Handle validation errors from User.create_user
            current_app.logger.error(f'Registration error: {str(e)}')
            flash(str(e), 'error')
        except Exception as e:
            # Handle unexpected errors
            current_app.logger.error(f'Unexpected registration error: {str(e)}')
            flash('An error occurred during registration. Please try again.', 'error')
            db.session.rollback()
    
    return render_template('auth/register.html', form=form, title='Create Account')


@auth_bp.route('/logout')
@login_required
def logout():
    """
    User logout endpoint.
    Clears user session and redirects to home page.
    """
    username = current_user.username
    current_app.logger.info(f'User logged out: {username}')
    
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """
    User profile view.
    Displays user information and profile completion status.
    """
    return render_template('auth/profile.html', user=current_user, title='My Profile')


@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    User profile edit endpoint.
    Allows users to update their profile information.
    """
    form = ProfileForm()
    
    # Prepopulate form with current user data
    if request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.address_line1.data = current_user.address_line1
        form.address_line2.data = current_user.address_line2
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.postal_code.data = current_user.postal_code
        form.country.data = current_user.country
    
    if form.validate_on_submit():
        try:
            # Check if email is being changed and is unique
            if form.email.data.lower() != current_user.email.lower():
                existing_user = User.query.filter_by(email=form.email.data.lower()).first()
                if existing_user:
                    flash('Email address is already in use.', 'error')
                    return render_template('auth/edit_profile.html', form=form, title='Edit Profile')
            
            # Update user information
            current_user.first_name = form.first_name.data.strip()
            current_user.last_name = form.last_name.data.strip()
            current_user.email = form.email.data.lower().strip()
            current_user.phone = form.phone.data.strip() if form.phone.data else None
            current_user.address_line1 = form.address_line1.data.strip() if form.address_line1.data else None
            current_user.address_line2 = form.address_line2.data.strip() if form.address_line2.data else None
            current_user.city = form.city.data.strip() if form.city.data else None
            current_user.state = form.state.data.strip() if form.state.data else None
            current_user.postal_code = form.postal_code.data.strip() if form.postal_code.data else None
            current_user.country = form.country.data.strip() if form.country.data else None
            
            db.session.commit()
            
            current_app.logger.info(f'Profile updated for user: {current_user.username}')
            flash('Your profile has been updated successfully!', 'success')
            return redirect(url_for('auth.profile'))
        
        except Exception as e:
            current_app.logger.error(f'Profile update error for {current_user.username}: {str(e)}')
            flash('An error occurred while updating your profile. Please try again.', 'error')
            db.session.rollback()
    
    return render_template('auth/edit_profile.html', form=form, title='Edit Profile')


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    Password change endpoint.
    Allows users to change their password with current password verification.
    """
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # Verify current password
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'error')
            return render_template('auth/change_password.html', form=form, title='Change Password')
        
        try:
            # Update password
            current_user.set_password(form.new_password.data)
            db.session.commit()
            
            current_app.logger.info(f'Password changed for user: {current_user.username}')
            flash('Your password has been changed successfully!', 'success')
            return redirect(url_for('auth.profile'))
        
        except Exception as e:
            current_app.logger.error(f'Password change error for {current_user.username}: {str(e)}')
            flash('An error occurred while changing your password. Please try again.', 'error')
            db.session.rollback()
    
    return render_template('auth/change_password.html', form=form, title='Change Password')


def merge_guest_cart_with_user_cart(user):
    """
    Merge guest cart items with user's cart upon login.
    
    Args:
        user: User instance to merge cart for
    """
    guest_session_id = session.get('cart_session_id')
    
    if not guest_session_id:
        return
    
    try:
        # Find guest cart
        guest_cart = Cart.query.filter_by(session_id=guest_session_id).first()
        if not guest_cart or guest_cart.is_empty():
            return
        
        # Get or create user cart
        user_cart = user.cart
        if not user_cart:
            user_cart = Cart(user_id=user.id)
            db.session.add(user_cart)
            db.session.flush()
        
        # Merge cart items
        merged_items = 0
        for guest_item in guest_cart.items:
            try:
                user_cart.add_item(guest_item.product_id, guest_item.quantity)
                merged_items += 1
            except ValueError:
                # Skip items that can't be added (out of stock, etc.)
                continue
        
        # Delete guest cart
        db.session.delete(guest_cart)
        db.session.commit()
        
        # Clear guest session
        session.pop('cart_session_id', None)
        
        if merged_items > 0:
            current_app.logger.info(f'Merged {merged_items} items from guest cart to user cart for: {user.username}')
            flash(f'{merged_items} items from your previous session have been added to your cart.', 'info')
    
    except Exception as e:
        current_app.logger.error(f'Error merging guest cart for user {user.username}: {str(e)}')
        db.session.rollback()
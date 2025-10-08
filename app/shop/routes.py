"""
Shop Routes.
Implements shopping functionality including product catalog, cart, and checkout.

Quality Management Principles:
- Session Management: Proper cart session handling
- Error Handling: Comprehensive error handling with user feedback
- Performance: Efficient database queries with pagination
- Security: Input validation and CSRF protection
- User Experience: Clear navigation and feedback
"""

import uuid
from flask import render_template, redirect, url_for, flash, request, session, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.models.product import Product, Category
from app.models.cart import Cart, CartItem
from app.models.order import Order
from app.models.user import User
from . import shop_bp
from .forms import AddToCartForm, UpdateCartForm, CheckoutForm, SearchForm


@shop_bp.route('/')
def index():
    """Shop homepage with featured products and categories."""
    try:
        # Get featured products
        featured_products = Product.get_featured(limit=8)
        
        # Get all active categories
        categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
        
        # Get latest products
        latest_products = Product.query.filter_by(is_active=True).order_by(
            Product.created_at.desc()
        ).limit(8).all()
        
        return render_template(
            'shop/index.html',
            featured_products=featured_products,
            latest_products=latest_products,
            categories=categories,
            title='Shop'
        )
    
    except Exception as e:
        current_app.logger.error(f'Error loading shop index: {str(e)}')
        return render_template('shop/index.html', title='Shop')


@shop_bp.route('/products')
def products():
    """Product listing with search and filtering."""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '', type=str)
    category_id = request.args.get('category', 0, type=int)
    sort_by = request.args.get('sort', 'name_asc', type=str)
    
    # Build base query
    query = Product.query.filter_by(is_active=True)
    
    # Apply search filter
    if search_query:
        search_pattern = f'%{search_query}%'
        query = query.filter(
            db.or_(
                Product.name.ilike(search_pattern),
                Product.description.ilike(search_pattern),
                Product.short_description.ilike(search_pattern)
            )
        )
    
    # Apply category filter
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Apply sorting
    if sort_by == 'name_desc':
        query = query.order_by(Product.name.desc())
    elif sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'newest':
        query = query.order_by(Product.created_at.desc())
    elif sort_by == 'oldest':
        query = query.order_by(Product.created_at.asc())
    else:  # name_asc
        query = query.order_by(Product.name.asc())
    
    # Paginate results
    products = query.paginate(
        page=page, 
        per_page=12, 
        error_out=False
    )
    
    # Get categories for filter
    categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
    
    # Create search form
    search_form = SearchForm()
    search_form.query.data = search_query
    search_form.category.data = category_id
    search_form.sort_by.data = sort_by
    
    return render_template(
        'shop/products.html',
        products=products,
        categories=categories,
        search_form=search_form,
        search_query=search_query,
        category_id=category_id,
        sort_by=sort_by,
        title='Products'
    )


@shop_bp.route('/product/<int:id>')
def product_detail(id):
    """Product detail page."""
    product = Product.query.filter_by(id=id, is_active=True).first_or_404()
    form = AddToCartForm()
    form.product_id.data = product.id
    
    # Get related products from same category
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()
    
    return render_template(
        'shop/product_detail.html',
        product=product,
        related_products=related_products,
        form=form,
        title=product.name
    )


@shop_bp.route('/cart')
def cart():
    """Shopping cart page."""
    cart = get_or_create_cart()
    
    if cart.is_empty():
        return render_template('shop/cart_empty.html', title='Shopping Cart')
    
    # Validate stock availability
    unavailable_items = cart.validate_stock_availability()
    
    return render_template(
        'shop/cart.html',
        cart=cart,
        unavailable_items=unavailable_items,
        title='Shopping Cart'
    )


@shop_bp.route('/cart/count')
def cart_count():
    """Get cart item count for AJAX requests."""
    cart = get_or_create_cart()
    return jsonify({'count': cart.get_total_items()})


@shop_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    """Add product to cart."""
    form = AddToCartForm()
    is_ajax = request.headers.get('Content-Type') == 'application/json' or request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if form.validate_on_submit():
        try:
            product_id = int(form.product_id.data)
            quantity = form.quantity.data
            
            # Get or create cart
            cart = get_or_create_cart()
            
            # Add item to cart
            cart.add_item(product_id, quantity)
            
            # Get product for flash message
            product = Product.query.get(product_id)
            message = f'Added {quantity} x {product.name} to cart!'
            
            if is_ajax:
                return jsonify({
                    'success': True,
                    'message': message,
                    'cart_count': cart.get_total_items(),
                    'cart_total': float(cart.get_total_amount())
                })
            else:
                flash(message, 'success')
                return redirect(url_for('shop.cart'))
        
        except ValueError as e:
            error_msg = str(e)
            if is_ajax:
                return jsonify({'success': False, 'message': error_msg}), 400
            else:
                flash(error_msg, 'error')
        except Exception as e:
            current_app.logger.error(f'Error adding to cart: {str(e)}')
            error_msg = 'An error occurred while adding item to cart.'
            if is_ajax:
                return jsonify({'success': False, 'message': error_msg}), 500
            else:
                flash(error_msg, 'error')
    
    else:
        error_msg = 'Invalid form data.'
        if is_ajax:
            return jsonify({'success': False, 'message': error_msg}), 400
        else:
            flash(error_msg, 'error')
    
    if not is_ajax:
        return redirect(request.referrer or url_for('shop.index'))


@shop_bp.route('/update-cart', methods=['POST'])
def update_cart():
    """Update cart item quantity."""
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', type=int)
    
    if not product_id or quantity is None:
        flash('Invalid request.', 'error')
        return redirect(url_for('shop.cart'))
    
    try:
        cart = get_or_create_cart()
        
        if quantity == 0:
            cart.remove_item(product_id)
            flash('Item removed from cart.', 'info')
        else:
            cart.update_item_quantity(product_id, quantity)
            flash('Cart updated successfully.', 'success')
    
    except ValueError as e:
        flash(str(e), 'error')
    except Exception as e:
        current_app.logger.error(f'Error updating cart: {str(e)}')
        flash('An error occurred while updating cart.', 'error')
    
    return redirect(url_for('shop.cart'))


@shop_bp.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    """Remove item from cart."""
    try:
        cart = get_or_create_cart()
        product = Product.query.get(product_id)
        cart.remove_item(product_id)
        if product:
            flash(f'"{product.name}" removed from cart.', 'info')
        else:
            flash('Item removed from cart.', 'info')
    
    except Exception as e:
        current_app.logger.error(f'Error removing from cart: {str(e)}')
        flash('An error occurred while removing item.', 'error')
    
    return redirect(url_for('shop.cart'))


@shop_bp.route('/clear-cart')
def clear_cart():
    """Clear all items from cart."""
    try:
        cart = get_or_create_cart()
        items_count = cart.get_total_items()
        cart.clear_cart()
        flash(f'All {items_count} items removed from cart.', 'info')
    
    except Exception as e:
        current_app.logger.error(f'Error clearing cart: {str(e)}')
        flash('An error occurred while clearing cart.', 'error')
    
    return redirect(url_for('shop.cart'))


@shop_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout process."""
    cart = get_or_create_cart()
    
    if cart.is_empty():
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('shop.cart'))
    
    # Validate stock availability
    unavailable_items = cart.validate_stock_availability()
    if unavailable_items:
        flash('Some items in your cart are no longer available. Please update your cart.', 'error')
        return redirect(url_for('shop.cart'))
    
    form = CheckoutForm()
    
    # Pre-populate form with user data
    if request.method == 'GET' and current_user.has_complete_profile():
        form.shipping_first_name.data = current_user.first_name
        form.shipping_last_name.data = current_user.last_name
        form.shipping_email.data = current_user.email
        form.shipping_phone.data = current_user.phone
        form.shipping_address_line1.data = current_user.address_line1
        form.shipping_address_line2.data = current_user.address_line2
        form.shipping_city.data = current_user.city
        form.shipping_state.data = current_user.state
        form.shipping_postal_code.data = current_user.postal_code
        form.shipping_country.data = current_user.country or 'United States'
    
    if form.validate_on_submit():
        try:
            # DUMMY IMPLEMENTATION - For demo purposes only
            import random
            import time
            
            # Simulate payment processing delay
            time.sleep(1)
            
            # Simulate payment success/failure (90% success rate for demo)
            payment_success = random.random() > 0.1
            
            if not payment_success:
                flash('Payment failed. Please try again with a different payment method.', 'error')
                return render_template(
                    'shop/checkout.html',
                    form=form,
                    cart=cart,
                    title='Checkout'
                )
            
            # Create shipping address
            shipping_address = {
                'first_name': form.shipping_first_name.data,
                'last_name': form.shipping_last_name.data,
                'email': form.shipping_email.data,
                'phone': form.shipping_phone.data,
                'address_line1': form.shipping_address_line1.data,
                'address_line2': form.shipping_address_line2.data,
                'city': form.shipping_city.data,
                'state': form.shipping_state.data,
                'postal_code': form.shipping_postal_code.data,
                'country': form.shipping_country.data
            }
            
            # Create dummy order
            order = Order.create_from_cart(
                user=current_user,
                cart=cart,
                shipping_address=shipping_address,
                payment_method=form.payment_method.data,
                notes=form.notes.data
            )
            
            # Clear cart after successful order
            cart.clear_cart()
            
            # Show success message with dummy tracking info
            flash(f'🎉 Order {order.order_number} placed successfully! Tracking ID: TRK{random.randint(100000, 999999)}', 'success')
            flash('This is a demo order - no actual payment was processed.', 'info')
            
            return redirect(url_for('shop.order_confirmation', order_id=order.id))
        
        except Exception as e:
            current_app.logger.error(f'Error processing checkout: {str(e)}')
            flash('An error occurred while processing your order. Please try again.', 'error')
            db.session.rollback()
    
    return render_template(
        'shop/checkout.html',
        form=form,
        cart=cart,
        title='Checkout'
    )


@shop_bp.route('/order-confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    """Order confirmation page."""
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    return render_template(
        'shop/order_confirmation.html',
        order=order,
        title='Order Confirmation'
    )


def get_or_create_cart():
    """Get or create cart for current user or session."""
    if current_user.is_authenticated:
        # Get user's cart
        cart = current_user.cart
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
        return cart
    else:
        # Get or create session cart
        session_id = session.get('cart_session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['cart_session_id'] = session_id
        
        cart = Cart.query.filter_by(session_id=session_id).first()
        if not cart:
            cart = Cart(session_id=session_id)
            db.session.add(cart)
            db.session.commit()
        
        return cart
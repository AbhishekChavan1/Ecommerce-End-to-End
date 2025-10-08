"""
Admin Routes.
Implements admin panel functionality for product and category management.

Quality Management Principles:
- Access Control: Admin-only access with proper authorization
- Data Validation: Comprehensive input validation and sanitization
- Error Handling: Robust error handling with user feedback
- Audit Trail: Logging of admin actions for accountability
- File Security: Safe image upload handling
"""

import os
import uuid
from flask import render_template, redirect, url_for, flash, request, current_app, abort, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from PIL import Image
from app import db
from app.models.product import Product, Category
from app.models.order import Order, OrderStatus
from app.models.user import User
from . import admin_bp
from .forms import ProductForm, CategoryForm, BulkUpdateForm


def admin_required(f):
    """Decorator to require admin access."""
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with key metrics."""
    try:
        # Get key metrics
        total_products = Product.query.count()
        active_products = Product.query.filter_by(is_active=True).count()
        total_categories = Category.query.count()
        total_users = User.query.count()
        
        # Recent orders
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
        
        # Low stock products
        low_stock_products = Product.get_low_stock_products()
        
        # Order statistics
        pending_orders = Order.query.filter_by(status=OrderStatus.PENDING).count()
        processing_orders = Order.query.filter_by(status=OrderStatus.PROCESSING).count()
        
        return render_template(
            'admin/dashboard.html',
            total_products=total_products,
            active_products=active_products,
            total_categories=total_categories,
            total_users=total_users,
            recent_orders=recent_orders,
            low_stock_products=low_stock_products,
            pending_orders=pending_orders,
            processing_orders=processing_orders,
            title='Admin Dashboard'
        )
    
    except Exception as e:
        current_app.logger.error(f'Error loading admin dashboard: {str(e)}')
        flash('Error loading dashboard data.', 'error')
        return render_template('admin/dashboard.html', title='Admin Dashboard')


# Product Management Routes
@admin_bp.route('/products')
@login_required
@admin_required
def products():
    """List all products with pagination and filtering."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    category_id = request.args.get('category', 0, type=int)
    status = request.args.get('status', 'all', type=str)
    
    # Build query
    query = Product.query
    
    # Apply filters
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if status == 'active':
        query = query.filter_by(is_active=True)
    elif status == 'inactive':
        query = query.filter_by(is_active=False)
    elif status == 'featured':
        query = query.filter_by(is_featured=True)
    elif status == 'low_stock':
        query = query.filter(Product.stock_quantity <= Product.min_stock_level)
    
    # Paginate results
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Get categories for filter
    categories = Category.query.filter_by(is_active=True).all()
    bulk_form = BulkUpdateForm()
    
    return render_template(
        'admin/products.html',
        products=products,
        categories=categories,
        bulk_form=bulk_form,
        search=search,
        category_id=category_id,
        status=status,
        title='Manage Products'
    )


@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    """Add new product."""
    form = ProductForm()
    
    if form.validate_on_submit():
        try:
            # Handle image upload
            image_filename = None
            if form.image.data:
                image_filename = save_product_image(form.image.data)
            
            # Create product
            product = Product(
                name=form.name.data.strip(),
                price=form.price.data,
                category_id=form.category_id.data,
                short_description=form.short_description.data.strip() if form.short_description.data else None,
                description=form.description.data.strip() if form.description.data else None,
                sku=form.sku.data.strip() if form.sku.data else None,
                cost_price=form.cost_price.data if form.cost_price.data else None,
                sale_price=form.sale_price.data if form.sale_price.data else None,
                stock_quantity=form.stock_quantity.data,
                min_stock_level=form.min_stock_level.data,
                weight=form.weight.data if form.weight.data else None,
                dimensions=form.dimensions.data.strip() if form.dimensions.data else None,
                image_filename=image_filename,
                is_active=form.is_active.data,
                is_featured=form.is_featured.data,
                is_digital=form.is_digital.data,
                meta_title=form.meta_title.data.strip() if form.meta_title.data else None,
                meta_description=form.meta_description.data.strip() if form.meta_description.data else None
            )
            
            db.session.add(product)
            db.session.commit()
            
            current_app.logger.info(f'Product created by {current_user.username}: {product.name}')
            flash(f'Product "{product.name}" has been created successfully!', 'success')
            return redirect(url_for('admin.products'))
        
        except Exception as e:
            current_app.logger.error(f'Error creating product: {str(e)}')
            flash('An error occurred while creating the product. Please try again.', 'error')
            db.session.rollback()
    
    return render_template('admin/product_form.html', form=form, title='Add Product')


@admin_bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):
    """Edit existing product."""
    product = Product.query.get_or_404(id)
    form = ProductForm()
    form.product_id = product.id  # For validation
    
    if form.validate_on_submit():
        try:
            # Handle image upload
            if form.image.data:
                # Delete old image
                if product.image_filename:
                    delete_product_image(product.image_filename)
                # Save new image
                product.image_filename = save_product_image(form.image.data)
            
            # Update product
            product.name = form.name.data.strip()
            product.short_description = form.short_description.data.strip() if form.short_description.data else None
            product.description = form.description.data.strip() if form.description.data else None
            product.sku = form.sku.data.strip() if form.sku.data else None
            product.category_id = form.category_id.data
            product.price = form.price.data
            product.cost_price = form.cost_price.data if form.cost_price.data else None
            product.sale_price = form.sale_price.data if form.sale_price.data else None
            product.stock_quantity = form.stock_quantity.data
            product.min_stock_level = form.min_stock_level.data
            product.weight = form.weight.data if form.weight.data else None
            product.dimensions = form.dimensions.data.strip() if form.dimensions.data else None
            product.is_active = form.is_active.data
            product.is_featured = form.is_featured.data
            product.is_digital = form.is_digital.data
            product.meta_title = form.meta_title.data.strip() if form.meta_title.data else None
            product.meta_description = form.meta_description.data.strip() if form.meta_description.data else None
            
            db.session.commit()
            
            current_app.logger.info(f'Product updated by {current_user.username}: {product.name}')
            flash(f'Product "{product.name}" has been updated successfully!', 'success')
            return redirect(url_for('admin.products'))
        
        except Exception as e:
            current_app.logger.error(f'Error updating product {id}: {str(e)}')
            flash('An error occurred while updating the product. Please try again.', 'error')
            db.session.rollback()
    
    # Pre-populate form with current product data
    elif request.method == 'GET':
        form.name.data = product.name
        form.short_description.data = product.short_description
        form.description.data = product.description
        form.sku.data = product.sku
        form.category_id.data = product.category_id
        form.price.data = float(product.price)
        form.cost_price.data = float(product.cost_price) if product.cost_price else None
        form.sale_price.data = float(product.sale_price) if product.sale_price else None
        form.stock_quantity.data = product.stock_quantity
        form.min_stock_level.data = product.min_stock_level
        form.weight.data = product.weight
        form.dimensions.data = product.dimensions
        form.is_active.data = product.is_active
        form.is_featured.data = product.is_featured
        form.is_digital.data = product.is_digital
        form.meta_title.data = product.meta_title
        form.meta_description.data = product.meta_description
    
    return render_template('admin/product_form.html', form=form, product=product, title='Edit Product')


@admin_bp.route('/products/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_product(id):
    """Delete product."""
    product = Product.query.get_or_404(id)
    
    try:
        # Delete product image if exists
        if product.image_filename:
            delete_product_image(product.image_filename)
        
        product_name = product.name
        db.session.delete(product)
        db.session.commit()
        
        current_app.logger.info(f'Product deleted by {current_user.username}: {product_name}')
        flash(f'Product "{product_name}" has been deleted successfully!', 'success')
    
    except Exception as e:
        current_app.logger.error(f'Error deleting product {id}: {str(e)}')
        flash('An error occurred while deleting the product. Please try again.', 'error')
        db.session.rollback()
    
    return redirect(url_for('admin.products'))


# Image handling functions
def save_product_image(image_file):
    """
    Save uploaded product image with processing.
    
    Args:
        image_file: FileStorage object from form
        
    Returns:
        str: Filename of saved image
    """
    if not image_file:
        return None
    
    # Generate unique filename
    filename = str(uuid.uuid4()) + '.' + image_file.filename.rsplit('.', 1)[1].lower()
    
    # Ensure upload directory exists
    upload_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    
    # Save file
    file_path = os.path.join(upload_path, filename)
    image_file.save(file_path)
    
    # Process image (resize, optimize)
    try:
        with Image.open(file_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if too large
            max_size = (800, 800)
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(file_path, 'JPEG', quality=85, optimize=True)
    
    except Exception as e:
        current_app.logger.error(f'Error processing image {filename}: {str(e)}')
    
    return filename


def delete_product_image(filename):
    """Delete product image file."""
    if not filename:
        return
    
    try:
        file_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        current_app.logger.error(f'Error deleting image {filename}: {str(e)}')


# Category Management Routes
@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    """List all categories."""
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', categories=categories, title='Manage Categories')


@admin_bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    """Add new category."""
    form = CategoryForm()
    
    if form.validate_on_submit():
        try:
            # Handle image upload
            image_filename = None
            if form.image.data:
                image_filename = save_product_image(form.image.data)
            
            # Create category
            category = Category(
                name=form.name.data.strip(),
                description=form.description.data.strip() if form.description.data else None,
                image_filename=image_filename,
                is_active=form.is_active.data
            )
            
            db.session.add(category)
            db.session.commit()
            
            current_app.logger.info(f'Category created by {current_user.username}: {category.name}')
            flash(f'Category "{category.name}" has been created successfully!', 'success')
            return redirect(url_for('admin.categories'))
        
        except Exception as e:
            current_app.logger.error(f'Error creating category: {str(e)}')
            flash('An error occurred while creating the category. Please try again.', 'error')
            db.session.rollback()
    
    return render_template('admin/category_form.html', form=form, title='Add Category')


@admin_bp.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(id):
    """Edit existing category."""
    category = Category.query.get_or_404(id)
    form = CategoryForm()
    form.category_id = category.id  # For validation
    
    if form.validate_on_submit():
        try:
            # Handle image upload
            if form.image.data:
                # Delete old image
                if category.image_filename:
                    delete_product_image(category.image_filename)
                # Save new image
                category.image_filename = save_product_image(form.image.data)
            
            # Update category
            category.name = form.name.data.strip()
            category.description = form.description.data.strip() if form.description.data else None
            category.is_active = form.is_active.data
            
            db.session.commit()
            
            current_app.logger.info(f'Category updated by {current_user.username}: {category.name}')
            flash(f'Category "{category.name}" has been updated successfully!', 'success')
            return redirect(url_for('admin.categories'))
        
        except Exception as e:
            current_app.logger.error(f'Error updating category {id}: {str(e)}')
            flash('An error occurred while updating the category. Please try again.', 'error')
            db.session.rollback()
    
    # Pre-populate form with current category data
    elif request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description
        form.is_active.data = category.is_active
    
    return render_template('admin/category_form.html', form=form, category=category, title='Edit Category')


@admin_bp.route('/categories/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(id):
    """Delete category."""
    category = Category.query.get_or_404(id)
    
    # Check if category has products
    if category.products:
        flash('Cannot delete category that contains products. Please move or delete products first.', 'error')
        return redirect(url_for('admin.categories'))
    
    try:
        # Delete category image if exists
        if category.image_filename:
            delete_product_image(category.image_filename)
        
        category_name = category.name
        db.session.delete(category)
        db.session.commit()
        
        current_app.logger.info(f'Category deleted by {current_user.username}: {category_name}')
        flash(f'Category "{category_name}" has been deleted successfully!', 'success')
    
    except Exception as e:
        current_app.logger.error(f'Error deleting category {id}: {str(e)}')
        flash('An error occurred while deleting the category. Please try again.', 'error')
        db.session.rollback()
    
    return redirect(url_for('admin.categories'))
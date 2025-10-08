"""
Main Routes.
Implements main application routes like home page and general pages.
"""

from flask import render_template, current_app
from app.models.product import Product, Category
from . import main_bp


@main_bp.route('/')
def index():
    """Home page with featured products."""
    try:
        # Get featured products
        featured_products = Product.get_featured(limit=8)
        
        # Get all categories for navigation
        categories = Category.query.filter_by(is_active=True).all()
        
        return render_template(
            'main/index.html',
            featured_products=featured_products,
            categories=categories,
            title='Welcome to Our Store'
        )
    
    except Exception as e:
        current_app.logger.error(f'Error loading home page: {str(e)}')
        return render_template('main/index.html', title='Welcome to Our Store')


@main_bp.route('/about')
def about():
    """About page."""
    return render_template('main/about.html', title='About Us')


@main_bp.route('/contact')
def contact():
    """Contact page."""
    return render_template('main/contact.html', title='Contact Us')
#!/usr/bin/env python3
"""
Sample Data Creation Script with Internet Images
Creates sample categories, products with real images, and users for development and testing.

Features:
- Real product images from Unsplash
- Comprehensive product catalog across multiple categories
- Admin and test users with proper permissions
- Realistic pricing and inventory data
- SEO-friendly product descriptions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.product import Product, Category
from app.models.user import User
from datetime import datetime
import requests
from urllib.parse import urlparse
import uuid


def create_sample_data():
    """Create sample data for the ecommerce application."""
    print("🚀 Creating Sample Data with Images...")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        # Create categories first
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Latest electronic gadgets and accessories',
                'slug': 'electronics'
            },
            {
                'name': 'Clothing',
                'description': 'Fashion and apparel for all occasions',
                'slug': 'clothing'
            },
            {
                'name': 'Books',
                'description': 'Educational and entertainment books',
                'slug': 'books'
            },
            {
                'name': 'Home & Garden',
                'description': 'Home improvement and gardening supplies',
                'slug': 'home-and-garden'
            },
            {
                'name': 'Sports & Fitness',
                'description': 'Sports equipment and fitness gear',
                'slug': 'sports-and-fitness'
            }
        ]
        
        print("Creating categories...")
        categories = {}
        
        for cat_data in categories_data:
            category = Category.query.filter_by(name=cat_data['name']).first()
            if not category:
                category = Category(
                    name=cat_data['name'],
                    description=cat_data['description'],
                    slug=cat_data['slug'],
                    is_active=True
                )
                db.session.add(category)
                db.session.commit()
                print(f"✅ Created category: {category.name}")
            else:
                print(f"📋 Category exists: {category.name}")
            
            categories[cat_data['name']] = category
        
        # Sample products data with real internet images
        products_data = [
            # Electronics
            {
                'name': 'Wireless Bluetooth Headphones',
                'description': 'High-quality wireless headphones with noise cancellation. Perfect for music lovers and professionals. Features 30-hour battery life and premium sound quality with crystal clear audio and deep bass.',
                'short_description': 'Premium wireless headphones with noise cancellation',
                'sku': 'ELC-WBH-001',
                'price': 199.99,
                'sale_price': 149.99,
                'stock_quantity': 25,
                'category': 'Electronics',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            {
                'name': 'Smartphone Stand',
                'description': 'Adjustable smartphone stand made from premium aluminum. Compatible with all phone sizes. Perfect for video calls, watching videos, and hands-free use. Sturdy construction with anti-slip base.',
                'short_description': 'Adjustable aluminum smartphone stand',
                'sku': 'ELC-SPS-002',
                'price': 29.99,
                'stock_quantity': 50,
                'category': 'Electronics',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1556656793-08538906a9f8?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            {
                'name': 'Portable Power Bank',
                'description': '20000mAh portable power bank with fast charging capability. Features multiple USB ports and LED indicator. Perfect for travel and outdoor activities. Compact design with safety protection.',
                'short_description': '20000mAh fast charging power bank',
                'sku': 'ELC-PPB-003',
                'price': 49.99,
                'stock_quantity': 35,
                'category': 'Electronics',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1609592806574-afb9c2bdf2c6?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            {
                'name': 'Wireless Mouse',
                'description': 'Ergonomic wireless mouse with precision tracking. Long battery life and comfortable grip for extended use. Works on multiple surfaces with optical precision.',
                'short_description': 'Ergonomic wireless mouse with precision tracking',
                'sku': 'ELC-WM-004',
                'price': 39.99,
                'stock_quantity': 40,
                'category': 'Electronics',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1527814050087-3793815479db?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            
            # Clothing
            {
                'name': 'Classic Cotton T-Shirt',
                'description': '100% premium cotton t-shirt. Comfortable fit with pre-shrunk fabric. Available in multiple colors and sizes. Perfect for casual wear and layering.',
                'short_description': '100% premium cotton comfort t-shirt',
                'sku': 'CLO-CCT-005',
                'price': 24.99,
                'stock_quantity': 100,
                'category': 'Clothing',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            {
                'name': 'Denim Jeans',
                'description': 'Classic fit denim jeans made from high-quality cotton blend. Durable construction with modern styling. Five-pocket design with reinforced stitching.',
                'short_description': 'Classic fit denim jeans',
                'sku': 'CLO-DJ-006',
                'price': 79.99,
                'sale_price': 59.99,
                'stock_quantity': 60,
                'category': 'Clothing',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            {
                'name': 'Winter Jacket',
                'description': 'Warm and stylish winter jacket with water-resistant coating. Perfect for cold weather with multiple pockets. Adjustable hood and cuffs for optimal comfort.',
                'short_description': 'Warm water-resistant winter jacket',
                'sku': 'CLO-WJ-007',
                'price': 149.99,
                'stock_quantity': 20,
                'category': 'Clothing',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            {
                'name': 'Running Shoes',
                'description': 'Comfortable running shoes with advanced cushioning technology. Breathable mesh upper and durable sole. Perfect for jogging, gym, and everyday activities.',
                'short_description': 'Advanced cushioning running shoes',
                'sku': 'CLO-RS-008',
                'price': 129.99,
                'stock_quantity': 45,
                'category': 'Clothing',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            
            # Books
            {
                'name': 'Python Programming Guide',
                'description': 'Comprehensive guide to Python programming for beginners and intermediate developers. Includes practical examples and exercises covering data structures, algorithms, and web development.',
                'short_description': 'Comprehensive Python programming guide',
                'sku': 'BOO-PPG-009',
                'price': 49.99,
                'stock_quantity': 30,
                'category': 'Books',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            {
                'name': 'Web Development Handbook',
                'description': 'Complete handbook covering HTML, CSS, JavaScript, and modern web development frameworks. Perfect for aspiring web developers with step-by-step tutorials and real-world projects.',
                'short_description': 'Complete web development handbook',
                'sku': 'BOO-WDH-010',
                'price': 59.99,
                'stock_quantity': 25,
                'category': 'Books',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            {
                'name': 'Business Strategy Book',
                'description': 'Learn proven business strategies from successful entrepreneurs and business leaders. Practical insights for business growth, marketing, and leadership development.',
                'short_description': 'Proven business strategies and insights',
                'sku': 'BOO-BSB-011',
                'price': 34.99,
                'stock_quantity': 40,
                'category': 'Books',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            
            # Home & Garden
            {
                'name': 'LED Desk Lamp',
                'description': 'Modern LED desk lamp with adjustable brightness and color temperature. Energy-efficient with sleek design. Touch controls and USB charging port included.',
                'short_description': 'Adjustable LED desk lamp',
                'sku': 'HGD-LDL-012',
                'price': 69.99,
                'stock_quantity': 30,
                'category': 'Home & Garden',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            {
                'name': 'Plant Pot Set',
                'description': 'Set of 3 ceramic plant pots with drainage holes. Perfect for indoor plants and herbs. Includes matching saucers and care instructions.',
                'short_description': 'Set of 3 ceramic plant pots',
                'sku': 'HGD-PPS-013',
                'price': 39.99,
                'stock_quantity': 50,
                'category': 'Home & Garden',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1485955900006-10f4d324d411?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            
            # Sports & Fitness
            {
                'name': 'Yoga Mat',
                'description': 'Premium non-slip yoga mat with excellent cushioning. Eco-friendly material with carrying strap included. Perfect for yoga, pilates, and floor exercises.',
                'short_description': 'Premium non-slip yoga mat',
                'sku': 'SPF-YM-014',
                'price': 29.99,
                'stock_quantity': 75,
                'category': 'Sports & Fitness',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            },
            {
                'name': 'Resistance Bands Set',
                'description': 'Complete resistance bands set with multiple resistance levels. Includes door anchor and exercise guide. Perfect for home workouts and strength training.',
                'short_description': 'Complete resistance bands set',
                'sku': 'SPF-RBS-015',
                'price': 34.99,
                'stock_quantity': 60,
                'category': 'Sports & Fitness',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80'
            }
        ]
        
        print("\nCreating products with images...")
        
        for product_data in products_data:
            # Check if product already exists
            existing_product = Product.query.filter_by(name=product_data['name']).first()
            if existing_product:
                # Update existing product with image URL
                existing_product.image_filename = product_data['image_url']
                db.session.commit()
                print(f"🔄 Updated product with image: {existing_product.name}")
                continue
            
            # Get category
            category = categories[product_data['category']]
            
            # Create product
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                short_description=product_data['short_description'],
                sku=product_data['sku'],
                slug=Product.generate_slug(product_data['name']),
                price=product_data['price'],
                sale_price=product_data.get('sale_price'),
                stock_quantity=product_data['stock_quantity'],
                min_stock_level=5,
                category_id=category.id,
                image_filename=product_data['image_url'],  # Store URL in image_filename
                is_active=True,
                is_featured=product_data.get('is_featured', False),
                is_digital=False
            )
            
            db.session.add(product)
            db.session.commit()
            print(f"✅ Created product: {product.name}")
        
        # Create admin user if not exists
        print("\nCreating users...")
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@example.com',
                first_name='Admin',
                last_name='User',
                country='United States',
                is_admin=True,
                is_active=True,
                email_confirmed=False
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print(f"✅ Created admin user: {admin_user.username}")
        
        # Check if testuser exists
        test_user = User.query.filter_by(username='testuser').first()
        if test_user:
            print(f"📋 Test user exists: {test_user.username}")
        
        print(f"\n{'='*50}")
        print("🎉 Sample data created successfully!")
        
        # Print summary
        category_count = Category.query.count()
        product_count = Product.query.count()
        user_count = User.query.count()
        
        print(f"📊 Categories: {category_count}")
        print(f"📦 Products: {product_count}")
        print(f"👥 Users: {user_count}")
        
        print(f"\n🔑 Login Credentials:")
        print(f"   Admin: admin / admin123")
        print(f"   User:  testuser / test123")


if __name__ == '__main__':
    create_sample_data()
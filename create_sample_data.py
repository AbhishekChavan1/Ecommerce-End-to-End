#!/usr/bin/env python3
"""
Sample Data Generator for E-commerce Application.
Creates sample categories and products for demonstration and testing.
"""

from app import create_app, db
from app.models.product import Product, Category
from app.models.user import User

def create_sample_data():
    """Create sample categories and products."""
    app = create_app('development')
    
    with app.app_context():
        print("🚀 Creating Sample Data...")
        print("=" * 50)
        
        # Clear existing data (optional - be careful in production!)
        # Product.query.delete()
        # Category.query.delete()
        
        # Create Categories
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Latest electronic devices and gadgets'
            },
            {
                'name': 'Clothing',
                'description': 'Fashion and apparel for all occasions'
            },
            {
                'name': 'Books',
                'description': 'Educational and entertainment books'
            },
            {
                'name': 'Home & Garden',
                'description': 'Home improvement and gardening supplies'
            },
            {
                'name': 'Sports & Fitness',
                'description': 'Sports equipment and fitness gear'
            }
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = Category.query.filter_by(name=cat_data['name']).first()
            if not category:
                category = Category(**cat_data)
                db.session.add(category)
                db.session.flush()  # To get the ID
                print(f"✅ Created category: {category.name}")
            else:
                print(f"📋 Category exists: {category.name}")
            categories[cat_data['name']] = category
        
        # Create Products
        products_data = [
            # Electronics
            {
                'name': 'Wireless Bluetooth Headphones',
                'description': 'High-quality wireless headphones with noise cancellation. Perfect for music lovers and professionals. Features 30-hour battery life and premium sound quality.',
                'short_description': 'Premium wireless headphones with noise cancellation',
                'price': 199.99,
                'sale_price': 149.99,
                'category': 'Electronics',
                'stock_quantity': 25,
                'is_featured': True,
                'sku': 'ELC-WBH-001'
            },
            {
                'name': 'Smartphone Stand',
                'description': 'Adjustable smartphone stand made from premium aluminum. Compatible with all phone sizes. Perfect for video calls, watching videos, and hands-free use.',
                'short_description': 'Adjustable aluminum smartphone stand',
                'price': 29.99,
                'category': 'Electronics',
                'stock_quantity': 50,
                'sku': 'ELC-SPS-002'
            },
            {
                'name': 'Portable Power Bank',
                'description': '20000mAh portable power bank with fast charging capability. Features multiple USB ports and LED indicator. Perfect for travel and outdoor activities.',
                'short_description': '20000mAh fast charging power bank',
                'price': 49.99,
                'category': 'Electronics',
                'stock_quantity': 35,
                'is_featured': True,
                'sku': 'ELC-PPB-003'
            },
            {
                'name': 'Wireless Mouse',
                'description': 'Ergonomic wireless mouse with precision tracking. Long battery life and comfortable grip for extended use.',
                'short_description': 'Ergonomic wireless mouse with precision tracking',
                'price': 39.99,
                'category': 'Electronics',
                'stock_quantity': 40,
                'sku': 'ELC-WM-004'
            },
            
            # Clothing
            {
                'name': 'Classic Cotton T-Shirt',
                'description': '100% premium cotton t-shirt. Comfortable fit with pre-shrunk fabric. Available in multiple colors and sizes.',
                'short_description': '100% premium cotton comfort t-shirt',
                'price': 24.99,
                'category': 'Clothing',
                'stock_quantity': 100,
                'sku': 'CLO-CCT-005'
            },
            {
                'name': 'Denim Jeans',
                'description': 'Classic fit denim jeans made from high-quality cotton blend. Durable construction with modern styling.',
                'short_description': 'Classic fit denim jeans',
                'price': 79.99,
                'sale_price': 59.99,
                'category': 'Clothing',
                'stock_quantity': 60,
                'is_featured': True,
                'sku': 'CLO-DJ-006'
            },
            {
                'name': 'Winter Jacket',
                'description': 'Warm and stylish winter jacket with water-resistant coating. Perfect for cold weather with multiple pockets.',
                'short_description': 'Warm water-resistant winter jacket',
                'price': 149.99,
                'category': 'Clothing',
                'stock_quantity': 20,
                'sku': 'CLO-WJ-007'
            },
            {
                'name': 'Running Shoes',
                'description': 'Comfortable running shoes with advanced cushioning technology. Breathable mesh upper and durable sole.',
                'short_description': 'Advanced cushioning running shoes',
                'price': 129.99,
                'category': 'Clothing',
                'stock_quantity': 45,
                'is_featured': True,
                'sku': 'CLO-RS-008'
            },
            
            # Books
            {
                'name': 'Python Programming Guide',
                'description': 'Comprehensive guide to Python programming for beginners and intermediate developers. Includes practical examples and exercises.',
                'short_description': 'Comprehensive Python programming guide',
                'price': 49.99,
                'category': 'Books',
                'stock_quantity': 30,
                'sku': 'BOO-PPG-009'
            },
            {
                'name': 'Web Development Handbook',
                'description': 'Complete handbook covering HTML, CSS, JavaScript, and modern web development frameworks. Perfect for aspiring web developers.',
                'short_description': 'Complete web development handbook',
                'price': 59.99,
                'category': 'Books',
                'stock_quantity': 25,
                'is_featured': True,
                'sku': 'BOO-WDH-010'
            },
            {
                'name': 'Business Strategy Book',
                'description': 'Learn proven business strategies from successful entrepreneurs and business leaders. Practical insights for business growth.',
                'short_description': 'Proven business strategies and insights',
                'price': 34.99,
                'category': 'Books',
                'stock_quantity': 40,
                'sku': 'BOO-BSB-011'
            },
            
            # Home & Garden
            {
                'name': 'LED Desk Lamp',
                'description': 'Modern LED desk lamp with adjustable brightness and color temperature. Energy-efficient with sleek design.',
                'short_description': 'Adjustable LED desk lamp',
                'price': 69.99,
                'category': 'Home & Garden',
                'stock_quantity': 30,
                'sku': 'HGD-LDL-012'
            },
            {
                'name': 'Plant Pot Set',
                'description': 'Set of 3 ceramic plant pots with drainage holes. Perfect for indoor plants and herbs. Includes saucers.',
                'short_description': 'Set of 3 ceramic plant pots',
                'price': 39.99,
                'category': 'Home & Garden',
                'stock_quantity': 50,
                'is_featured': True,
                'sku': 'HGD-PPS-013'
            },
            
            # Sports & Fitness
            {
                'name': 'Yoga Mat',
                'description': 'Premium non-slip yoga mat with excellent cushioning. Eco-friendly material with carrying strap included.',
                'short_description': 'Premium non-slip yoga mat',
                'price': 29.99,
                'category': 'Sports & Fitness',
                'stock_quantity': 75,
                'sku': 'SPF-YM-014'
            },
            {
                'name': 'Resistance Bands Set',
                'description': 'Complete resistance bands set with multiple resistance levels. Includes door anchor and exercise guide.',
                'short_description': 'Complete resistance bands set',
                'price': 34.99,
                'category': 'Sports & Fitness',
                'stock_quantity': 60,
                'is_featured': True,
                'sku': 'SPF-RBS-015'
            }
        ]
        
        # Create Products
        for prod_data in products_data:
            category_name = prod_data.pop('category')
            category = categories[category_name]
            
            product = Product.query.filter_by(name=prod_data['name']).first()
            if not product:
                product = Product(
                    category_id=category.id,
                    **prod_data
                )
                db.session.add(product)
                print(f"✅ Created product: {product.name}")
            else:
                print(f"📋 Product exists: {product.name}")
        
        # Create a test admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                is_admin=True
            )
            print(f"✅ Created admin user: {admin.username}")
        else:
            print(f"📋 Admin user exists: {admin.username}")
        
        # Create a test regular user if it doesn't exist
        user = User.query.filter_by(username='testuser').first()
        if not user:
            user = User.create_user(
                username='testuser',
                email='test@example.com',
                password='test123',
                first_name='Test',
                last_name='User'
            )
            print(f"✅ Created test user: {user.username}")
        else:
            print(f"📋 Test user exists: {user.username}")
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "=" * 50)
        print("🎉 Sample data created successfully!")
        print(f"📊 Categories: {Category.query.count()}")
        print(f"📦 Products: {Product.query.count()}")
        print(f"👥 Users: {User.query.count()}")
        print("\n🔑 Login Credentials:")
        print("   Admin: admin / admin123")
        print("   User:  testuser / test123")

if __name__ == "__main__":
    create_sample_data()
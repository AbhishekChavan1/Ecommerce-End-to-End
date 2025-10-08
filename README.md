# E-Commerce Web Application

A comprehensive, modular e-commerce web application built with Flask, implementing modern web development best practices and Software Quality Management (SQM) principles.

## 🚀 Features

### Core Functionality
- **User Management**: Registration, authentication, profile management
- **Product Catalog**: Browse, search, filter products with categories
- **Shopping Cart**: Add/remove items, quantity management, persistent cart
- **Checkout Process**: Secure order placement with shipping information
- **Admin Panel**: Complete CRUD operations for products, categories, and orders
- **Responsive Design**: Mobile-first Bootstrap 5 interface

### Technical Features
- **Modular Architecture**: Flask Blueprints for organized code structure
- **Database ORM**: SQLAlchemy with relationship management
- **Security**: CSRF protection, password hashing, secure sessions
- **File Upload**: Image handling with validation and processing
- **Search & Filtering**: Advanced product search with multiple criteria
- **Pagination**: Efficient data loading for large datasets

## 🏗️ Architecture

### Project Structure
```
ecommerce_app/
├── app/                    # Application package
│   ├── __init__.py        # App factory and configuration
│   ├── models/            # Database models
│   │   ├── user.py       # User and authentication
│   │   ├── product.py    # Product and category models
│   │   ├── cart.py       # Shopping cart functionality
│   │   └── order.py      # Order management
│   ├── auth/             # Authentication blueprint
│   │   ├── routes.py     # Auth routes (login, register, logout)
│   │   └── forms.py      # Authentication forms
│   ├── main/             # Main application blueprint
│   │   └── routes.py     # Home page and general routes
│   ├── shop/             # Shopping functionality blueprint
│   │   ├── routes.py     # Product browsing, cart, checkout
│   │   └── forms.py      # Shopping forms
│   └── admin/            # Admin panel blueprint
│       ├── routes.py     # Admin CRUD operations
│       └── forms.py      # Admin forms
├── templates/            # Jinja2 templates
│   ├── base.html        # Base template with navigation
│   ├── auth/            # Authentication templates
│   ├── main/            # Main page templates
│   ├── shop/            # Shopping templates
│   └── admin/           # Admin panel templates
├── static/              # Static files
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── uploads/        # User uploaded images
├── tests/              # Test suite
│   ├── unit/           # Unit tests
│   ├── selenium/       # UI automation tests
│   └── conftest.py     # Test configuration
├── config/             # Configuration files
├── instance/           # Instance-specific files
├── requirements.txt    # Python dependencies
├── run.py             # Application entry point
└── README.md          # This file
```

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.3.3
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login with bcrypt password hashing
- **Forms**: Flask-WTF with CSRF protection
- **Environment**: python-dotenv for configuration

### Frontend
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.0
- **JavaScript**: jQuery for AJAX interactions
- **Templates**: Jinja2 templating engine

### Testing
- **Unit Testing**: pytest with Flask-specific fixtures
- **UI Testing**: Selenium WebDriver with Page Object Model
- **Test Data**: Faker and Factory Boy for realistic test data
- **Coverage**: pytest-cov for code coverage analysis

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Chrome/Chromium browser (for Selenium tests)
- Git (for version control)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ecommerce_app
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///ecommerce.db

# Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216

# Admin User
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

### 5. Initialize Database
```bash
# Initialize Flask-Migrate
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade

# Create admin user and sample data
flask create-admin
flask init-db
```

### 6. Run the Application
```bash
# Development server
flask run

# Or using Python directly
python run.py
```

The application will be available at `http://localhost:5000`

## 🧪 Testing

### Running Unit Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_user_model.py
```

### Running Selenium Tests
```bash
# Run UI tests
pytest tests/selenium/

# Run in headless mode
pytest tests/selenium/ --headless

# Run specific test class
pytest tests/selenium/test_ecommerce_ui.py::TestUserAuthentication
```

### Test Coverage Report
```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

## 🔐 Security Features

### Authentication & Authorization
- Password hashing using bcrypt
- Session-based authentication with Flask-Login
- CSRF protection on all forms
- Admin-only access controls
- Secure cookie configuration

### Data Validation
- Server-side form validation with WTForms
- Email format validation
- File upload restrictions and validation
- SQL injection prevention through ORM
- XSS protection via template escaping

### Security Headers
- Content Security Policy (CSP)
- X-Frame-Options protection
- Secure session cookies
- HTTPS enforcement in production

## 📊 Software Quality Management (SQM) Implementation

### Code Quality
- **Modular Design**: Separation of concerns with Flask Blueprints
- **DRY Principle**: Reusable components and templates
- **SOLID Principles**: Well-structured classes and methods
- **PEP 8 Compliance**: Python coding standards adherence

### Testing Strategy
- **Test Pyramid**: Unit tests, integration tests, and UI tests
- **Page Object Model**: Maintainable Selenium test structure
- **Test Data Management**: Factories and fixtures for consistent test data
- **Continuous Testing**: Automated test execution

### Documentation
- **Code Comments**: Inline documentation for complex logic
- **API Documentation**: Clear method and class documentation
- **User Documentation**: Comprehensive README and setup guides
- **Test Documentation**: Test case descriptions and coverage reports

### Error Handling
- **Graceful Degradation**: Proper error handling and user feedback
- **Logging**: Comprehensive application logging
- **Exception Management**: Structured error handling with appropriate responses
- **Input Validation**: Multiple layers of data validation

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Application environment (development/production)
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string
- `UPLOAD_FOLDER`: File upload directory
- `MAX_CONTENT_LENGTH`: Maximum file upload size

### Database Configuration
- SQLite for development (file-based)
- PostgreSQL/MySQL support for production
- Automatic table creation and migrations
- Sample data initialization

## 📱 API Endpoints

### Public Endpoints
- `GET /`: Home page
- `GET /auth/login`: User login
- `POST /auth/login`: Process login
- `GET /auth/register`: User registration
- `POST /auth/register`: Process registration
- `GET /shop/products`: Product listing
- `GET /shop/product/<id>`: Product details

### Authenticated Endpoints
- `POST /shop/add-to-cart`: Add item to cart
- `GET /shop/cart`: View shopping cart
- `POST /shop/checkout`: Process checkout
- `GET /auth/profile`: User profile
- `POST /auth/logout`: User logout

### Admin Endpoints
- `GET /admin/dashboard`: Admin dashboard
- `GET /admin/products`: Manage products
- `POST /admin/products/add`: Add new product
- `PUT /admin/products/<id>`: Update product
- `DELETE /admin/products/<id>`: Delete product

## 🚢 Deployment

### Production Checklist
1. Set `FLASK_ENV=production`
2. Configure secure `SECRET_KEY`
3. Use production database (PostgreSQL/MySQL)
4. Enable SSL/HTTPS
5. Configure proper file permissions
6. Set up reverse proxy (Nginx)
7. Use WSGI server (Gunicorn)
8. Configure logging
9. Set up monitoring
10. Regular security updates

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 coding standards
- Write comprehensive tests for new features
- Update documentation for API changes
- Use meaningful commit messages
- Ensure all tests pass before submitting PR

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Comprehensive guides in the `/docs` directory
- **Community**: Join our discussion forums for help and tips

## 🔄 Version History

### v1.0.0 (Current)
- Initial release with core e-commerce functionality
- User authentication and authorization
- Product catalog with search and filtering
- Shopping cart and checkout process
- Admin panel for content management
- Comprehensive test suite with Selenium automation
- Responsive Bootstrap UI

### Planned Features
- Payment gateway integration
- Email notifications
- Product reviews and ratings
- Inventory management
- Order tracking
- Multi-vendor support
- Advanced analytics dashboard

## 🏆 Acknowledgments

- Flask team for the excellent web framework
- Bootstrap team for the responsive CSS framework
- Selenium project for web automation capabilities
- SQLAlchemy for the robust ORM
- Open source community for inspiration and tools

---

**Built with ❤️ using Flask and modern web technologies**
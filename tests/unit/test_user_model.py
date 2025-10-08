"""
Unit Tests for User Model.
Tests user authentication, profile management, and validation.

Quality Management Principles:
- Comprehensive Coverage: Tests all user functionality
- Edge Case Testing: Tests boundary conditions and error cases
- Security Testing: Tests password hashing and authentication
- Data Validation: Tests input validation and constraints
"""

import pytest
from app.models.user import User
from app import db

# Mark all unit tests
pytestmark = pytest.mark.unit


class TestUserModel:
    """Test cases for User model."""
    
    def test_user_creation(self, clean_db):
        """Test basic user creation."""
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('TestPassword123')
        
        clean_db.session.add(user)
        clean_db.session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.get_full_name() == 'Test User'
        assert user.is_admin is False
        assert user.is_active is True
    
    def test_password_hashing(self, clean_db):
        """Test password hashing and verification."""
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        password = 'TestPassword123'
        user.set_password(password)
        
        # Password should be hashed
        assert user.password_hash is not None
        assert user.password_hash != password
        
        # Should verify correct password
        assert user.check_password(password) is True
        
        # Should not verify incorrect password
        assert user.check_password('WrongPassword') is False
    
    def test_user_authentication(self, clean_db, sample_user):
        """Test user authentication method."""
        # Test authentication with username
        user = User.authenticate(sample_user.username, 'TestPassword123')
        assert user is not None
        assert user.id == sample_user.id
        
        # Test authentication with email
        user = User.authenticate(sample_user.email, 'TestPassword123')
        assert user is not None
        assert user.id == sample_user.id
        
        # Test failed authentication
        user = User.authenticate(sample_user.username, 'WrongPassword')
        assert user is None
        
        # Test authentication with non-existent user
        user = User.authenticate('nonexistent', 'TestPassword123')
        assert user is None
    
    def test_user_create_user_method(self, clean_db):
        """Test User.create_user class method."""
        user = User.create_user(
            username='newuser',
            email='new@example.com',
            password='NewPassword123',
            first_name='New',
            last_name='User'
        )
        
        assert user.id is not None
        assert user.username == 'newuser'
        assert user.email == 'new@example.com'
        assert user.check_password('NewPassword123') is True
    
    def test_duplicate_username_validation(self, clean_db, sample_user):
        """Test that duplicate usernames raise ValueError."""
        with pytest.raises(ValueError, match="Username .* already exists"):
            User.create_user(
                username=sample_user.username,  # Duplicate username
                email='different@example.com',
                password='TestPassword123',
                first_name='Test',
                last_name='User'
            )
    
    def test_duplicate_email_validation(self, clean_db, sample_user):
        """Test that duplicate emails raise ValueError."""
        with pytest.raises(ValueError, match="Email .* already exists"):
            User.create_user(
                username='differentuser',
                email=sample_user.email,  # Duplicate email
                password='TestPassword123',
                first_name='Test',
                last_name='User'
            )
    
    def test_user_profile_completion(self, clean_db):
        """Test profile completion checking."""
        # User without complete profile
        user = User(
            username='incomplete',
            email='incomplete@example.com',
            first_name='Incomplete',
            last_name='User'
        )
        assert user.has_complete_profile() is False
        
        # User with complete profile
        complete_user = User(
            username='complete',
            email='complete@example.com',
            first_name='Complete',
            last_name='User',
            phone='555-0123',
            address_line1='123 Main St',
            city='Test City',
            state='TS',
            postal_code='12345'
        )
        assert complete_user.has_complete_profile() is True
    
    def test_user_address_formatting(self, clean_db, sample_user):
        """Test address formatting."""
        address = sample_user.get_address()
        expected_lines = [
            '123 Test St',
            'Test City, TS 12345',
            'Test Country'
        ]
        
        for line in expected_lines:
            assert line in address
    
    def test_user_to_dict(self, clean_db, sample_user):
        """Test user dictionary conversion."""
        user_dict = sample_user.to_dict()
        
        assert user_dict['id'] == sample_user.id
        assert user_dict['username'] == sample_user.username
        assert user_dict['email'] == sample_user.email
        assert user_dict['full_name'] == sample_user.get_full_name()
        assert user_dict['is_admin'] == sample_user.is_admin
        assert 'password_hash' not in user_dict  # Should not expose password
    
    def test_inactive_user_authentication(self, clean_db):
        """Test that inactive users cannot authenticate."""
        user = User.create_user(
            username='inactive',
            email='inactive@example.com',
            password='TestPassword123',
            first_name='Inactive',
            last_name='User',
            is_active=False
        )
        
        # Inactive user should not authenticate
        authenticated_user = User.authenticate('inactive', 'TestPassword123')
        assert authenticated_user is None
    
    def test_admin_user_creation(self, clean_db):
        """Test admin user creation."""
        admin = User.create_user(
            username='admin',
            email='admin@example.com',
            password='AdminPassword123',
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
        
        assert admin.is_admin is True
        assert admin.to_dict()['is_admin'] is True
    
    def test_user_string_representations(self, clean_db, sample_user):
        """Test string representations of user."""
        assert str(sample_user) == 'Test User (testuser)'
        assert 'testuser' in repr(sample_user)
    
    def test_flask_login_properties(self, clean_db, sample_user):
        """Test Flask-Login required properties."""
        assert sample_user.is_authenticated is True
        assert sample_user.is_anonymous is False
        assert sample_user.get_id() == str(sample_user.id)
    
    def test_last_login_update(self, clean_db, sample_user):
        """Test last login timestamp update."""
        original_last_login = sample_user.last_login
        sample_user.update_last_login()
        
        assert sample_user.last_login is not None
        assert sample_user.last_login != original_last_login
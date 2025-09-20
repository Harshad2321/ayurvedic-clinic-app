"""
Secure Configuration Module for Ayurvedic Clinic
Handles environment variables and secure settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class with secure defaults"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-dev-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Authentication (secure - from environment)
    CLINIC_MOBILE = os.getenv('CLINIC_MOBILE', '0000000000')  # Fallback for dev
    CLINIC_PIN = os.getenv('CLINIC_PIN', '0000')  # Fallback for dev
    
    # Support Contact Information
    SUPPORT_NAME = os.getenv('SUPPORT_NAME', 'Technical Support')
    SUPPORT_PHONE = os.getenv('SUPPORT_PHONE', '0000000000')
    SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL', 'support@clinic.com')
    
    # Clinic Information
    DOCTOR_NAME = os.getenv('DOCTOR_NAME', 'Dr. [Name]')
    CLINIC_NAME = os.getenv('CLINIC_NAME', 'Ayurvedic Clinic')
    CLINIC_ADDRESS = os.getenv('CLINIC_ADDRESS', 'Clinic Address')
    CLINIC_EMAIL = os.getenv('CLINIC_EMAIL', 'clinic@example.com')
    CLINIC_PHONE = os.getenv('CLINIC_PHONE', '9898143702')
    
    @classmethod
    def get_auth_credentials(cls):
        """Get authentication credentials securely"""
        return {
            'mobile': cls.CLINIC_MOBILE,
            'pin': cls.CLINIC_PIN
        }
    
    @classmethod
    def get_support_contact(cls):
        """Get support contact information"""
        return {
            'name': cls.SUPPORT_NAME,
            'phone': cls.SUPPORT_PHONE,
            'email': cls.SUPPORT_EMAIL,
            'role': 'Technical Support & App Administrator'
        }
    
    @classmethod
    def get_clinic_details(cls):
        """Get clinic details"""
        return {
            'doctor_name': cls.DOCTOR_NAME,
            'clinic_name': cls.CLINIC_NAME,
            'address': cls.CLINIC_ADDRESS,
            'email': cls.CLINIC_EMAIL,
            'phone': cls.CLINIC_PHONE
        }

# Production Configuration
class ProductionConfig(Config):
    """Production-specific configuration"""
    DEBUG = False
    
    @classmethod
    def validate_config(cls):
        """Validate that all required environment variables are set"""
        required_vars = [
            'SECRET_KEY', 'CLINIC_MOBILE', 'CLINIC_PIN',
            'SUPPORT_NAME', 'SUPPORT_PHONE', 'SUPPORT_EMAIL'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True

# Development Configuration
class DevelopmentConfig(Config):
    """Development-specific configuration"""
    DEBUG = True

# Configuration factory
def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig
    else:
        return DevelopmentConfig
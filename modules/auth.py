"""
Simple authentication system for Ayurvedic Clinic
Secure login for clinic staff using environment variables
"""

from functools import wraps
from flask import session, request, redirect, url_for, flash
from config import get_config

# Get secure configuration
config = get_config()

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please login to access the clinic management system', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def verify_credentials(mobile, pin):
    """Verify login credentials using secure configuration"""
    credentials = config.get_auth_credentials()
    return (mobile == credentials['mobile'] and pin == credentials['pin'])

def get_clinic_info():
    """Get clinic and doctor information from secure configuration"""
    clinic_details = config.get_clinic_details()
    support_contact = config.get_support_contact()
    
    return {
        'name': clinic_details['clinic_name'],
        'tagline': 'Traditional Healing for Modern Wellness',
        'doctor_name': clinic_details['doctor_name'],
        'qualifications': 'BAMS, MD (Ayurveda)',  # Update with actual qualifications
        'experience': '15+ Years',  # Update with actual experience
        'specializations': [
            'Panchakarma Treatments',
            'Chronic Disease Management', 
            'Women\'s Health',
            'Digestive Disorders',
            'Stress & Anxiety Treatment',
            'Lifestyle Counseling'
        ],
        'services': [
            {
                'name': 'Traditional Consultation',
                'description': 'Comprehensive Ayurvedic health assessment with pulse diagnosis'
            },
            {
                'name': 'Panchakarma Therapy',
                'description': 'Complete detoxification and rejuvenation treatments'
            },
            {
                'name': 'Herbal Medicine',
                'description': 'Custom herbal formulations for various health conditions'
            },
            {
                'name': 'Dietary Counseling',
                'description': 'Personalized nutrition guidance based on Ayurvedic principles'
            },
            {
                'name': 'Lifestyle Guidance',
                'description': 'Daily routine and seasonal lifestyle recommendations'
            }
        ],
        'phone': config.CLINIC_MOBILE,  # Using the same mobile for clinic contact
        'email': clinic_details['email'],
        'address': clinic_details['address'],
        'operating_hours': {
            'monday': '9:00 AM - 6:00 PM',
            'tuesday': '9:00 AM - 6:00 PM',
            'wednesday': '9:00 AM - 6:00 PM',
            'thursday': '9:00 AM - 6:00 PM',
            'friday': '9:00 AM - 6:00 PM',
            'saturday': '9:00 AM - 2:00 PM',
            'sunday': 'Closed'
        },
        'philosophy': 'We believe in the ancient wisdom of Ayurveda combined with modern understanding to provide holistic healthcare. Our approach focuses on treating the root cause of illness while promoting overall wellness through natural healing methods, personalized treatments, and lifestyle guidance.',
        'support_contact': support_contact
    }
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
        'tagline': 'Traditional Ayurvedic Healing & Wellness - Women-Owned Clinic',
        'doctor_name': clinic_details['doctor_name'],
        'qualifications': 'BAMS, MD (Ayurveda)',  # Update with actual qualifications
        'experience': '15+ Years',  # Update with actual experience
        'specializations': [
            'Traditional Ayurvedic Consultation',
            'Panchakarma Treatments',
            'Chronic Disease Management', 
            'Women\'s Health & Wellness',
            'Digestive Disorders',
            'Stress & Anxiety Treatment',
            'Lifestyle & Dietary Counseling'
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
            },
            {
                'name': 'Women\'s Health',
                'description': 'Specialized Ayurvedic care for women\'s health concerns'
            }
        ],
        'phone': clinic_details['phone'],
        'email': clinic_details['email'],
        'address': clinic_details['address'],
        'location': 'Vapi, Gujarat',
        'coordinates': '9W92+Q3 Vapi, Gujarat',
        'rating': '5.0 stars (Google Reviews)',
        'business_type': 'Women-Owned Ayurvedic Clinic',
        'operating_hours': {
            'monday': '9:30 AM - 2:00 PM, 5:00 PM - 8:30 PM',
            'tuesday': '9:30 AM - 2:00 PM, 5:00 PM - 8:30 PM',
            'wednesday': '9:30 AM - 2:00 PM, 5:00 PM - 8:30 PM',
            'thursday': '9:30 AM - 2:00 PM, 5:00 PM - 8:30 PM',
            'friday': '9:30 AM - 2:00 PM, 5:00 PM - 8:30 PM',
            'saturday': '9:30 AM - 2:00 PM, 5:00 PM - 8:30 PM',
            'sunday': 'Closed'
        },
        'philosophy': 'Dhanvantari Clinic is a women-owned Ayurvedic practice located in the heart of Vapi, Gujarat. We believe in the ancient wisdom of Ayurveda combined with modern understanding to provide holistic healthcare. Our approach focuses on treating the root cause of illness while promoting overall wellness through natural healing methods, personalized treatments, and comprehensive lifestyle guidance.',
        'support_contact': support_contact
    }
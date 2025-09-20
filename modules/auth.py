"""
Simple authentication system for Ayurvedic Clinic
Secure login for clinic staff
"""

from functools import wraps
from flask import session, request, redirect, url_for, flash

# Clinic credentials (in production, use environment variables)
CLINIC_CREDENTIALS = {
    'mobile': '9898143702',
    'pin': '1234'  # Simple 4-digit PIN for easy mobile use
}

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
    """Verify login credentials"""
    return (mobile == CLINIC_CREDENTIALS['mobile'] and 
            pin == CLINIC_CREDENTIALS['pin'])

def get_clinic_info():
    """Get clinic and doctor information"""
    return {
        'name': 'Dr. Harsh\'s Ayurvedic Clinic',
        'tagline': 'Traditional Healing for Modern Wellness',
        'doctor_name': 'Harsh',  # Update this with mom's name
        'qualifications': 'BAMS, MD (Ayurveda)',  # Update with her qualifications
        'experience': '15+ Years',  # Update with her experience
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
        'phone': '9898143702',
        'email': 'clinic@ayurveda.com',  # Update with actual email
        'address': 'Ayurvedic Clinic Address, City, State - 123456',  # Update address
        'operating_hours': {
            'monday': '9:00 AM - 6:00 PM',
            'tuesday': '9:00 AM - 6:00 PM',
            'wednesday': '9:00 AM - 6:00 PM',
            'thursday': '9:00 AM - 6:00 PM',
            'friday': '9:00 AM - 6:00 PM',
            'saturday': '9:00 AM - 2:00 PM',
            'sunday': 'Closed'
        },
        'philosophy': 'We believe in the ancient wisdom of Ayurveda combined with modern understanding to provide holistic healthcare. Our approach focuses on treating the root cause of illness while promoting overall wellness through natural healing methods, personalized treatments, and lifestyle guidance.'
    }
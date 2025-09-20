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
        'doctor_name': 'Dr. [Your Mom\'s Name]',  # Update this with her name
        'qualifications': 'BAMS, MD (Ayurveda)',  # Update with her qualifications
        'specialization': 'Ayurvedic Medicine & Panchakarma',
        'experience': '15+ Years',  # Update with her experience
        'clinic_name': 'Shanti Ayurvedic Clinic',  # Update clinic name
        'address': 'Your Clinic Address, City, State - 123456',  # Update address
        'phone': '9898143702',
        'consultation_hours': 'Mon-Sat: 9:00 AM - 6:00 PM',
        'specialties': [
            'Panchakarma Treatments',
            'Chronic Disease Management', 
            'Women\'s Health',
            'Digestive Disorders',
            'Stress & Anxiety Treatment',
            'Lifestyle Counseling'
        ]
    }
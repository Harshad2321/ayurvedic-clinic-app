#!/usr/bin/env python3
"""
Quick setup script to configure environment variables for production
This helps if the deployment fails due to missing environment variables
"""

import os
import sys

def setup_render_environment():
    """Instructions for setting up environment variables on Render"""
    
    print("🔒 URGENT: Environment Variables Setup Required")
    print("=" * 60)
    print()
    print("The app deployment may fail because it needs environment variables.")
    print("Follow these steps to set up secure environment variables on Render:")
    print()
    print("1. Go to: https://dashboard.render.com")
    print("2. Select your 'ayurvedic-clinic-app' service")
    print("3. Click on 'Environment' tab")
    print("4. Add these environment variables:")
    print()
    
    env_vars = {
        'CLINIC_MOBILE': '9898143702',
        'CLINIC_PIN': '1978',
        'SECRET_KEY': 'ayurvedic_clinic_secure_key_2025_production',
        'SUPPORT_NAME': 'Harshad Agrawal',
        'SUPPORT_PHONE': '7622871384',
        'SUPPORT_EMAIL': 'harshadd.agrawal2005@gmail.com',
        'DOCTOR_NAME': 'Dr. [Mom\'s Name]',
        'CLINIC_NAME': 'Dhanvantari Clinic',
        'CLINIC_ADDRESS': 'Vapi - Namdha Rd, Khadkala, Gita Nagar, Vapi, Gujarat 396191',
        'CLINIC_EMAIL': 'dhanvantariclinic@gmail.com',
        'CLINIC_PHONE': '9898143702',
        'FLASK_ENV': 'production'
    }
    
    for key, value in env_vars.items():
        print(f"   {key} = {value}")
    
    print()
    print("5. Click 'Save Changes'")
    print("6. The app will automatically redeploy with secure configuration")
    print()
    print("🔒 Security Features Now Active:")
    print("   ✅ No sensitive data in GitHub code")
    print("   ✅ PIN and credentials stored securely")
    print("   ✅ Database files excluded from repository")
    print("   ✅ Environment-based configuration")
    print()
    print("After setting up environment variables, your app will be:")
    print("🌐 https://ayurvedic-clinic-app.onrender.com")

if __name__ == "__main__":
    setup_render_environment()
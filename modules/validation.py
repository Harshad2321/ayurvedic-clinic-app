"""
Validation utilities for Ayurvedic Clinic Management System
Provides comprehensive data validation functions
"""

import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime, date

def validate_patient_data(name: str, age: int, gender: str, phone: str, 
                         weight: Optional[float] = None, conditions: Optional[str] = None) -> Tuple[bool, List[str]]:
    """
    Validate patient data comprehensively
    Returns: (is_valid: bool, error_messages: List[str])
    """
    errors = []
    
    # Name validation
    if not name or not name.strip():
        errors.append("Patient name is required")
    elif len(name.strip()) < 2:
        errors.append("Patient name must be at least 2 characters long")
    elif len(name.strip()) > 100:
        errors.append("Patient name cannot exceed 100 characters")
    elif not re.match(r"^[a-zA-Z\s.',-]+$", name.strip()):
        errors.append("Patient name can only contain letters, spaces, and common punctuation")
    
    # Age validation
    if age is None:
        errors.append("Patient age is required")
    elif not isinstance(age, int):
        errors.append("Age must be a valid number")
    elif age < 0:
        errors.append("Age cannot be negative")
    elif age > 150:
        errors.append("Age cannot exceed 150 years")
    
    # Gender validation
    valid_genders = ['male', 'female', 'other']
    if not gender or gender.lower() not in valid_genders:
        errors.append("Please select a valid gender (Male, Female, or Other)")
    
    # Phone validation
    if not phone or not phone.strip():
        errors.append("Phone number is required")
    else:
        # Remove all non-digit characters for validation
        phone_digits = re.sub(r'[^\d]', '', phone.strip())
        if len(phone_digits) != 10:
            errors.append("Phone number must be exactly 10 digits")
        elif not phone_digits.isdigit():
            errors.append("Phone number can only contain digits")
        elif phone_digits[0] == '0':
            errors.append("Phone number cannot start with 0")
    
    # Weight validation (optional)
    if weight is not None:
        if not isinstance(weight, (int, float)):
            errors.append("Weight must be a valid number")
        elif weight <= 0:
            errors.append("Weight must be greater than 0")
        elif weight > 500:
            errors.append("Weight cannot exceed 500 kg")
    
    # Conditions validation (optional)
    if conditions and len(conditions.strip()) > 500:
        errors.append("Medical conditions description cannot exceed 500 characters")
    
    return len(errors) == 0, errors

def validate_visit_data(visit_date: str, symptoms: Optional[str] = None, 
                       medicines: Optional[str] = None, diet_notes: Optional[str] = None,
                       weight: Optional[float] = None, blood_pressure: Optional[str] = None,
                       notes: Optional[str] = None) -> Tuple[bool, List[str]]:
    """
    Validate visit data
    Returns: (is_valid: bool, error_messages: List[str])
    """
    errors = []
    
    # Visit date validation
    if not visit_date:
        errors.append("Visit date is required")
    else:
        try:
            visit_date_obj = datetime.strptime(visit_date, '%Y-%m-%d').date()
            today = date.today()
            
            # Check if date is too far in the future
            if visit_date_obj > today:
                # Allow up to 7 days in the future for appointment scheduling
                days_ahead = (visit_date_obj - today).days
                if days_ahead > 7:
                    errors.append("Visit date cannot be more than 7 days in the future")
            
            # Check if date is too far in the past (more than 10 years)
            if (today - visit_date_obj).days > 3650:
                errors.append("Visit date cannot be more than 10 years in the past")
                
        except ValueError:
            errors.append("Invalid date format. Please use a valid date")
    
    # Weight validation (optional)
    if weight is not None:
        if not isinstance(weight, (int, float)):
            errors.append("Weight must be a valid number")
        elif weight <= 0:
            errors.append("Weight must be greater than 0")
        elif weight > 500:
            errors.append("Weight cannot exceed 500 kg")
    
    # Blood pressure validation (optional)
    if blood_pressure and blood_pressure.strip():
        bp_pattern = r'^\d{2,3}/\d{2,3}$'
        if not re.match(bp_pattern, blood_pressure.strip()):
            errors.append("Blood pressure must be in format: 120/80")
        else:
            try:
                systolic, diastolic = map(int, blood_pressure.split('/'))
                if systolic < 50 or systolic > 300:
                    errors.append("Systolic pressure must be between 50-300")
                if diastolic < 30 or diastolic > 200:
                    errors.append("Diastolic pressure must be between 30-200")
                if systolic <= diastolic:
                    errors.append("Systolic pressure must be higher than diastolic")
            except ValueError:
                errors.append("Invalid blood pressure format")
    
    # Text field validations
    text_fields = {
        'symptoms': symptoms,
        'medicines': medicines,
        'diet_notes': diet_notes,
        'notes': notes
    }
    
    for field_name, field_value in text_fields.items():
        if field_value and len(field_value.strip()) > 1000:
            field_display = field_name.replace('_', ' ').title()
            errors.append(f"{field_display} cannot exceed 1000 characters")
    
    return len(errors) == 0, errors

def validate_search_term(search_term: str) -> Tuple[bool, List[str]]:
    """
    Validate search input
    Returns: (is_valid: bool, error_messages: List[str])
    """
    errors = []
    
    if not search_term or not search_term.strip():
        errors.append("Please enter a search term")
    elif len(search_term.strip()) < 2:
        errors.append("Search term must be at least 2 characters long")
    elif len(search_term.strip()) > 50:
        errors.append("Search term cannot exceed 50 characters")
    
    return len(errors) == 0, errors

def sanitize_input(text: str) -> str:
    """
    Sanitize text input to prevent issues
    """
    if not text:
        return ""
    
    # Strip whitespace
    text = text.strip()
    
    # Remove any potentially harmful characters (basic XSS prevention)
    text = re.sub(r'[<>"]', '', text)
    
    return text

def format_phone_number(phone: str) -> str:
    """
    Format phone number consistently
    """
    if not phone:
        return ""
    
    # Remove all non-digit characters
    phone_digits = re.sub(r'[^\d]', '', phone.strip())
    
    # Return 10-digit format
    if len(phone_digits) == 10:
        return phone_digits
    
    return phone  # Return original if not valid

def validate_phone_uniqueness(phone: str, exclude_patient_id: Optional[int] = None) -> bool:
    """
    Check if phone number is unique (would need database import)
    This is a placeholder - to be implemented with database checking
    """
    # This would connect to database and check for duplicates
    # For now, return True (assuming unique)
    return True

def get_validation_summary(errors: List[str]) -> Dict[str, any]:
    """
    Create a user-friendly validation summary
    """
    if not errors:
        return {
            'is_valid': True,
            'message': 'All data is valid',
            'errors': [],
            'error_count': 0
        }
    
    return {
        'is_valid': False,
        'message': f"Please fix {len(errors)} error{'s' if len(errors) > 1 else ''}:",
        'errors': errors,
        'error_count': len(errors)
    }
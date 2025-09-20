"""
Database module for Ayurvedic Clinic Management System
Handles SQLite database operations for patients and visits
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'clinic.db')

def format_date_for_display(date_str: str) -> str:
    """Convert date from YYYY-MM-DD to DD/MM/YYYY format for display"""
    try:
        if date_str:
            date_obj = datetime.strptime(date_str[:10], '%Y-%m-%d')
            return date_obj.strftime('%d/%m/%Y')
        return ""
    except:
        return date_str

def format_date_for_storage(date_str: str) -> str:
    """Convert date from DD/MM/YYYY to YYYY-MM-DD format for storage"""
    try:
        if '/' in date_str:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            return date_obj.strftime('%Y-%m-%d')
        return date_str
    except:
        return date_str

def get_today_formatted() -> str:
    """Get today's date in DD/MM/YYYY format"""
    return datetime.now().strftime('%d/%m/%Y')

def init_database():
    """Initialize the database and create tables if they don't exist"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                weight REAL,
                conditions TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create visits table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                visit_date DATE NOT NULL,
                symptoms TEXT,
                medicines TEXT,
                diet_notes TEXT,
                weight REAL,
                blood_pressure TEXT,
                notes TEXT,
                created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
            )
        ''')
        
        # Create audit log table for enterprise tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                table_name TEXT NOT NULL,
                record_id INTEGER,
                old_data TEXT,
                new_data TEXT,
                user_id TEXT DEFAULT 'system',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                details TEXT
            )
        ''')
        
        # Create soft deletion tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deleted_records (
                deletion_id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                record_id INTEGER NOT NULL,
                original_data TEXT NOT NULL,
                deleted_by TEXT DEFAULT 'system',
                deletion_reason TEXT,
                deletion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                can_restore BOOLEAN DEFAULT 1
            )
        ''')
        
        # Add deleted flag to existing tables if not exists
        cursor.execute('''
            ALTER TABLE patients ADD COLUMN is_deleted BOOLEAN DEFAULT 0
        ''')
        
        cursor.execute('''
            ALTER TABLE visits ADD COLUMN is_deleted BOOLEAN DEFAULT 0
        ''')
        
        conn.commit()
        conn.close()
        return True, "Database initialized successfully"
    
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            # Columns already exist, this is fine
            try:
                conn.close()
            except:
                pass
            return True, "Database initialized successfully"
        return False, f"Error initializing database: {str(e)}"
    
    except Exception as e:
        return False, f"Error initializing database: {str(e)}"

def add_patient(name: str, age: int, gender: str, phone: str, weight: float = None, conditions: str = None, registration_date: str = None) -> Tuple[bool, str, int]:
    """
    Add a new patient to the database
    Returns: (success: bool, message: str, patient_id: int)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if phone number already exists
        cursor.execute("SELECT patient_id FROM patients WHERE phone = ?", (phone,))
        if cursor.fetchone():
            conn.close()
            return False, "Phone number already exists", 0
        
        # Use current date if no registration date provided
        if not registration_date:
            registration_date = datetime.now().strftime('%Y-%m-%d')
        
        # Insert new patient
        cursor.execute('''
            INSERT INTO patients (name, age, gender, phone, weight, conditions, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, gender, phone, weight, conditions, registration_date))
        
        patient_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return True, f"Patient {name} added successfully on {registration_date}", patient_id
    
    except Exception as e:
        return False, f"Error adding patient: {str(e)}", 0

def search_patients(search_term: str) -> List[Dict]:
    """
    Search for patients by name or phone number
    Returns list of patient dictionaries
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Search by name or phone (case insensitive)
        search_pattern = f"%{search_term}%"
        cursor.execute('''
            SELECT patient_id, name, age, gender, phone, weight, conditions, created_date
            FROM patients 
            WHERE LOWER(name) LIKE LOWER(?) OR phone LIKE ?
            ORDER BY name
        ''', (search_pattern, search_pattern))
        
        results = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        patients = []
        for row in results:
            patients.append({
                'patient_id': row[0],
                'name': row[1],
                'age': row[2],
                'gender': row[3],
                'phone': row[4],
                'weight': row[5],
                'conditions': row[6],
                'created_date': row[7],
                'created_date_formatted': format_date_for_display(row[7])
            })
        
        return patients
    
    except Exception as e:
        print(f"Error searching patients: {str(e)}")
        return []

def get_patient_by_id(patient_id: int) -> Optional[Dict]:
    """Get patient details by patient ID"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT patient_id, name, age, gender, phone, weight, conditions, created_date
            FROM patients WHERE patient_id = ?
        ''', (patient_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'patient_id': result[0],
                'name': result[1],
                'age': result[2],
                'gender': result[3],
                'phone': result[4],
                'weight': result[5],
                'conditions': result[6],
                'created_date': result[7],
                'created_date_formatted': format_date_for_display(result[7])
            }
        return None
    
    except Exception as e:
        print(f"Error getting patient: {str(e)}")
        return None

def find_existing_patient_by_phone(phone: str) -> Optional[Dict]:
    """
    Check if a patient with this phone number already exists
    Returns patient data if found, None otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT patient_id, name, age, gender, phone, weight, conditions, created_date
            FROM patients 
            WHERE phone = ?
        ''', (phone,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'patient_id': result[0],
                'name': result[1],
                'age': result[2],
                'gender': result[3],
                'phone': result[4],
                'weight': result[5],
                'conditions': result[6],
                'created_date': result[7],
                'created_date_formatted': format_date_for_display(result[7])
            }
        return None
    
    except Exception as e:
        print(f"Error checking for existing patient: {str(e)}")
        return None

def find_similar_patients(name: str, phone: str) -> List[Dict]:
    """
    Find patients with similar names or exact phone match
    Used for duplicate detection during patient registration
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check for exact phone match or similar name
        name_pattern = f"%{name}%"
        cursor.execute('''
            SELECT patient_id, name, age, gender, phone, weight, conditions, created_date
            FROM patients 
            WHERE phone = ? OR LOWER(name) LIKE LOWER(?)
            ORDER BY 
                CASE WHEN phone = ? THEN 0 ELSE 1 END,
                name
        ''', (phone, name_pattern, phone))
        
        results = cursor.fetchall()
        conn.close()
        
        patients = []
        for row in results:
            patients.append({
                'patient_id': row[0],
                'name': row[1],
                'age': row[2],
                'gender': row[3],
                'phone': row[4],
                'weight': row[5],
                'conditions': row[6],
                'created_date': row[7],
                'created_date_formatted': format_date_for_display(row[7]),
                'is_phone_match': row[4] == phone,
                'is_name_similar': name.lower() in row[1].lower() or row[1].lower() in name.lower()
            })
        
        return patients
    
    except Exception as e:
        print(f"Error finding similar patients: {str(e)}")
        return []

def merge_patient_records(keep_patient_id: int, duplicate_patient_id: int) -> Tuple[bool, str]:
    """
    Merge two patient records - transfer all visits from duplicate to keep patient, then delete duplicate
    Returns: (success: bool, message: str)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get patient names for the message
        cursor.execute('SELECT name FROM patients WHERE patient_id = ?', (keep_patient_id,))
        keep_name = cursor.fetchone()
        cursor.execute('SELECT name FROM patients WHERE patient_id = ?', (duplicate_patient_id,))
        duplicate_name = cursor.fetchone()
        
        if not keep_name or not duplicate_name:
            conn.close()
            return False, "One or both patients not found"
        
        keep_name = keep_name[0]
        duplicate_name = duplicate_name[0]
        
        # Transfer all visits from duplicate to keep patient
        cursor.execute('''
            UPDATE visits 
            SET patient_id = ? 
            WHERE patient_id = ?
        ''', (keep_patient_id, duplicate_patient_id))
        
        visits_transferred = cursor.rowcount
        
        # Delete the duplicate patient record
        cursor.execute('DELETE FROM patients WHERE patient_id = ?', (duplicate_patient_id,))
        
        conn.commit()
        conn.close()
        
        message = f"Successfully merged {duplicate_name} into {keep_name}. Transferred {visits_transferred} visits."
        return True, message
    
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Error merging patients: {str(e)}"

def update_patient_info(patient_id: int, name: str = None, age: int = None, gender: str = None, 
                       phone: str = None, weight: float = None, conditions: str = None) -> Tuple[bool, str]:
    """
    Update patient information
    Returns: (success: bool, message: str)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Build update query dynamically based on provided parameters
        update_fields = []
        values = []
        
        if name is not None:
            update_fields.append("name = ?")
            values.append(name)
        if age is not None:
            update_fields.append("age = ?")
            values.append(age)
        if gender is not None:
            update_fields.append("gender = ?")
            values.append(gender)
        if phone is not None:
            update_fields.append("phone = ?")
            values.append(phone)
        if weight is not None:
            update_fields.append("weight = ?")
            values.append(weight)
        if conditions is not None:
            update_fields.append("conditions = ?")
            values.append(conditions)
        
        if not update_fields:
            conn.close()
            return False, "No fields to update"
        
        # Add patient_id to values for WHERE clause
        values.append(patient_id)
        
        query = f"UPDATE patients SET {', '.join(update_fields)} WHERE patient_id = ?"
        cursor.execute(query, values)
        
        if cursor.rowcount == 0:
            conn.close()
            return False, "Patient not found"
        
        conn.commit()
        conn.close()
        
        return True, "Patient information updated successfully"
    
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Error updating patient: {str(e)}"

def add_visit(patient_id: int, visit_date: str, symptoms: str = None, medicines: str = None, 
              diet_notes: str = None, weight: float = None, blood_pressure: str = None, 
              notes: str = None) -> Tuple[bool, str]:
    """
    Add a new visit for a patient
    Returns: (success: bool, message: str)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verify patient exists
        cursor.execute("SELECT patient_id FROM patients WHERE patient_id = ?", (patient_id,))
        if not cursor.fetchone():
            conn.close()
            return False, "Patient not found"
        
        # Convert date format if needed (DD/MM/YYYY to YYYY-MM-DD for storage)
        storage_date = format_date_for_storage(visit_date)
        
        # Insert new visit
        cursor.execute('''
            INSERT INTO visits (patient_id, visit_date, symptoms, medicines, diet_notes, 
                              weight, blood_pressure, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (patient_id, storage_date, symptoms, medicines, diet_notes, weight, blood_pressure, notes))
        
        conn.commit()
        conn.close()
        
        return True, f"Visit added successfully for {format_date_for_display(storage_date)}"
    
    except Exception as e:
        return False, f"Error adding visit: {str(e)}"

def get_patient_visits(patient_id: int) -> List[Dict]:
    """
    Get all visits for a specific patient
    Returns list of visit dictionaries sorted by date (newest first)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT visit_id, visit_date, symptoms, medicines, diet_notes, 
                   weight, blood_pressure, notes, created_timestamp
            FROM visits 
            WHERE patient_id = ? AND (is_deleted = 0 OR is_deleted IS NULL)
            ORDER BY visit_date DESC, created_timestamp DESC
        ''', (patient_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        visits = []
        for row in results:
            visits.append({
                'visit_id': row[0],
                'visit_date': row[1],
                'visit_date_formatted': format_date_for_display(row[1]),
                'symptoms': row[2],
                'medicines': row[3],
                'diet_notes': row[4],
                'weight': row[5],
                'blood_pressure': row[6],
                'notes': row[7],
                'created_timestamp': row[8]
            })
        
        return visits
    
    except Exception as e:
        print(f"Error getting patient visits: {str(e)}")
        return []

def get_all_patients() -> List[Dict]:
    """Get all patients from the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT patient_id, name, age, gender, phone, weight, conditions, created_date
            FROM patients 
            ORDER BY name
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        patients = []
        for row in results:
            patients.append({
                'patient_id': row[0],
                'name': row[1],
                'age': row[2],
                'gender': row[3],
                'phone': row[4],
                'weight': row[5],
                'conditions': row[6],
                'created_date': row[7],
                'created_date_formatted': format_date_for_display(row[7])
            })
        
        return patients
    
    except Exception as e:
        print(f"Error getting all patients: {str(e)}")
        return []

def update_patient(patient_id: int, name: str = None, age: int = None, gender: str = None, 
                  phone: str = None, weight: float = None, conditions: str = None) -> Tuple[bool, str]:
    """Update patient information"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Build dynamic update query
        updates = []
        values = []
        
        if name is not None:
            updates.append("name = ?")
            values.append(name)
        if age is not None:
            updates.append("age = ?")
            values.append(age)
        if gender is not None:
            updates.append("gender = ?")
            values.append(gender)
        if phone is not None:
            updates.append("phone = ?")
            values.append(phone)
        if weight is not None:
            updates.append("weight = ?")
            values.append(weight)
        if conditions is not None:
            updates.append("conditions = ?")
            values.append(conditions)
        
        if not updates:
            conn.close()
            return False, "No updates provided"
        
        updates.append("updated_date = CURRENT_TIMESTAMP")
        values.append(patient_id)
        
        query = f"UPDATE patients SET {', '.join(updates)} WHERE patient_id = ?"
        cursor.execute(query, values)
        
        if cursor.rowcount == 0:
            conn.close()
            return False, "Patient not found"
        
        conn.commit()
        conn.close()
        
        return True, "Patient updated successfully"
    
    except Exception as e:
        return False, f"Error updating patient: {str(e)}"

def get_patient_weight_progression(patient_id: int) -> List[Dict]:
    """
    Get weight progression for a patient from visits and initial registration
    Returns list of weight records with dates
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get initial weight from patient registration
        cursor.execute('''
            SELECT weight, created_date FROM patients WHERE patient_id = ?
        ''', (patient_id,))
        
        patient_data = cursor.fetchone()
        weight_records = []
        
        if patient_data and patient_data[0]:
            weight_records.append({
                'date': patient_data[1][:10],  # Extract date part
                'weight': patient_data[0],
                'type': 'Registration'
            })
        
        # Get weights from visits
        cursor.execute('''
            SELECT visit_date, weight FROM visits 
            WHERE patient_id = ? AND weight IS NOT NULL
            ORDER BY visit_date ASC
        ''', (patient_id,))
        
        visit_weights = cursor.fetchall()
        
        for row in visit_weights:
            weight_records.append({
                'date': row[0],
                'weight': row[1],
                'type': 'Visit'
            })
        
        conn.close()
        
        # Sort by date
        weight_records.sort(key=lambda x: x['date'])
        return weight_records
    
    except Exception as e:
        print(f"Error getting weight progression: {str(e)}")
        return []

def get_patient_visit_count(patient_id: int) -> int:
    """Get the total number of visits for a patient"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM visits WHERE patient_id = ?", (patient_id,))
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    except Exception as e:
        print(f"Error getting visit count: {str(e)}")
        return 0

def get_patient_summary(patient_id: int) -> Dict:
    """Get patient summary with visit count and last visit info"""
    try:
        patient = get_patient_by_id(patient_id)
        if not patient:
            return None
        
        visit_count = get_patient_visit_count(patient_id)
        visits = get_patient_visits(patient_id)
        
        last_visit = None
        last_weight = None
        
        if visits:
            last_visit = visits[0]  # Most recent visit
            # Get last recorded weight (from visit or registration)
            for visit in visits:
                if visit['weight']:
                    last_weight = visit['weight']
                    break
            if not last_weight:
                last_weight = patient['weight']
        
        return {
            'patient': patient,
            'visit_count': visit_count,
            'last_visit': last_visit,
            'last_weight': last_weight,
            'is_new_patient': visit_count == 0,
            'is_returning_patient': visit_count > 0
        }
    
    except Exception as e:
        print(f"Error getting patient summary: {str(e)}")
        return None

def search_patients_with_visit_info(search_term: str) -> List[Dict]:
    """Search patients and include visit count information"""
    try:
        patients = search_patients(search_term)
        
        # Add visit count to each patient
        for patient in patients:
            patient['visit_count'] = get_patient_visit_count(patient['patient_id'])
            patient['is_new_patient'] = patient['visit_count'] == 0
            patient['is_returning_patient'] = patient['visit_count'] > 0
        
        return patients
    
    except Exception as e:
        print(f"Error searching patients with visit info: {str(e)}")
        return []

def get_database_stats() -> Dict:
    """Get basic statistics about the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get patient count
        cursor.execute("SELECT COUNT(*) FROM patients")
        patient_count = cursor.fetchone()[0]
        
        # Get visit count
        cursor.execute("SELECT COUNT(*) FROM visits")
        visit_count = cursor.fetchone()[0]
        
        # Get recent patients (last 7 days)
        cursor.execute('''
            SELECT COUNT(*) FROM patients 
            WHERE created_date >= date('now', '-7 days')
        ''')
        recent_patients = cursor.fetchone()[0]
        
        # Get recent visits (last 7 days)
        cursor.execute('''
            SELECT COUNT(*) FROM visits 
            WHERE visit_date >= date('now', '-7 days')
        ''')
        recent_visits = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_patients': patient_count,
            'total_visits': visit_count,
            'recent_patients': recent_patients,
            'recent_visits': recent_visits
        }
    
    except Exception as e:
        print(f"Error getting database stats: {str(e)}")
        return {
            'total_patients': 0,
            'total_visits': 0,
            'recent_patients': 0,
            'recent_visits': 0
        }

# ==========================================
# ENTERPRISE AUDIT AND DELETION SYSTEM
# ==========================================

def log_audit_action(action: str, table_name: str, record_id: int = None, 
                    old_data: str = None, new_data: str = None, 
                    user_id: str = 'system', details: str = None) -> bool:
    """
    Log all database actions for enterprise audit trail
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_log (action, table_name, record_id, old_data, new_data, user_id, details)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (action, table_name, record_id, old_data, new_data, user_id, details))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error logging audit action: {str(e)}")
        return False

def soft_delete_patient(patient_id: int, reason: str = None, user_id: str = 'system') -> Tuple[bool, str]:
    """
    Soft delete a patient (mark as deleted but keep data for audit)
    Returns: (success: bool, message: str)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get patient data before deletion
        cursor.execute('SELECT * FROM patients WHERE patient_id = ? AND is_deleted = 0', (patient_id,))
        patient_data = cursor.fetchone()
        
        if not patient_data:
            conn.close()
            return False, "Patient not found or already deleted"
        
        # Get visit count for confirmation
        cursor.execute('SELECT COUNT(*) FROM visits WHERE patient_id = ? AND is_deleted = 0', (patient_id,))
        visit_count = cursor.fetchone()[0]
        
        patient_name = patient_data[1]  # Assuming name is second column
        
        # Store original data in JSON format
        import json
        original_data = {
            'patient_id': patient_data[0],
            'name': patient_data[1],
            'age': patient_data[2],
            'gender': patient_data[3],
            'phone': patient_data[4],
            'weight': patient_data[5],
            'conditions': patient_data[6],
            'created_date': patient_data[7],
            'visit_count_at_deletion': visit_count
        }
        
        # Mark patient as deleted
        cursor.execute('''
            UPDATE patients 
            SET is_deleted = 1 
            WHERE patient_id = ?
        ''', (patient_id,))
        
        # Mark all visits as deleted
        cursor.execute('''
            UPDATE visits 
            SET is_deleted = 1 
            WHERE patient_id = ?
        ''', (patient_id,))
        
        # Log in deleted_records table
        cursor.execute('''
            INSERT INTO deleted_records (table_name, record_id, original_data, deleted_by, deletion_reason)
            VALUES (?, ?, ?, ?, ?)
        ''', ('patients', patient_id, json.dumps(original_data), user_id, reason))
        
        conn.commit()
        conn.close()
        
        # Log audit action
        log_audit_action('DELETE', 'patients', patient_id, 
                        json.dumps(original_data), None, user_id, 
                        f"Soft deleted patient '{patient_name}' with {visit_count} visits. Reason: {reason}")
        
        return True, f"Patient '{patient_name}' and {visit_count} visits marked as deleted successfully"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Error deleting patient: {str(e)}"

def hard_delete_patient(patient_id: int, confirmation_code: str, user_id: str = 'system') -> Tuple[bool, str]:
    """
    PERMANENT deletion - only for extreme cases with confirmation
    Returns: (success: bool, message: str)
    """
    expected_code = f"DELETE-{patient_id}-PERMANENT"
    
    if confirmation_code != expected_code:
        return False, f"Invalid confirmation code. Required: {expected_code}"
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get patient data before deletion
        cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
        patient_data = cursor.fetchone()
        
        if not patient_data:
            conn.close()
            return False, "Patient not found"
        
        patient_name = patient_data[1]
        
        # Store in audit log before permanent deletion
        import json
        original_data = {
            'patient_id': patient_data[0],
            'name': patient_data[1],
            'age': patient_data[2],
            'gender': patient_data[3],
            'phone': patient_data[4],
            'weight': patient_data[5],
            'conditions': patient_data[6],
            'created_date': patient_data[7]
        }
        
        # Delete all visits permanently
        cursor.execute('DELETE FROM visits WHERE patient_id = ?', (patient_id,))
        deleted_visits = cursor.rowcount
        
        # Delete patient permanently
        cursor.execute('DELETE FROM patients WHERE patient_id = ?', (patient_id,))
        
        conn.commit()
        conn.close()
        
        # Log audit action
        log_audit_action('HARD_DELETE', 'patients', patient_id, 
                        json.dumps(original_data), None, user_id, 
                        f"PERMANENT deletion of patient '{patient_name}' and {deleted_visits} visits")
        
        return True, f"Patient '{patient_name}' and {deleted_visits} visits permanently deleted"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Error permanently deleting patient: {str(e)}"

def soft_delete_visit(visit_id: int, reason: str = None, user_id: str = 'system') -> Tuple[bool, str]:
    """
    Soft delete a specific visit
    Returns: (success: bool, message: str)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get visit data
        cursor.execute('SELECT * FROM visits WHERE visit_id = ? AND is_deleted = 0', (visit_id,))
        visit_data = cursor.fetchone()
        
        if not visit_data:
            conn.close()
            return False, "Visit not found or already deleted"
        
        # Get patient name for context
        cursor.execute('SELECT name FROM patients WHERE patient_id = ?', (visit_data[1],))
        patient_name = cursor.fetchone()[0]
        
        # Store original data
        import json
        original_data = {
            'visit_id': visit_data[0],
            'patient_id': visit_data[1],
            'visit_date': visit_data[2],
            'symptoms': visit_data[3],
            'medicines': visit_data[4],
            'diet_notes': visit_data[5],
            'weight': visit_data[6],
            'blood_pressure': visit_data[7],
            'notes': visit_data[8]
        }
        
        # Mark visit as deleted
        cursor.execute('UPDATE visits SET is_deleted = 1 WHERE visit_id = ?', (visit_id,))
        
        # Log in deleted_records
        cursor.execute('''
            INSERT INTO deleted_records (table_name, record_id, original_data, deleted_by, deletion_reason)
            VALUES (?, ?, ?, ?, ?)
        ''', ('visits', visit_id, json.dumps(original_data), user_id, reason))
        
        conn.commit()
        conn.close()
        
        # Log audit action
        log_audit_action('DELETE', 'visits', visit_id, 
                        json.dumps(original_data), None, user_id, 
                        f"Deleted visit for patient '{patient_name}'. Reason: {reason}")
        
        return True, f"Visit for '{patient_name}' on {visit_data[2]} marked as deleted"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Error deleting visit: {str(e)}"

def restore_deleted_patient(patient_id: int, user_id: str = 'system') -> Tuple[bool, str]:
    """
    Restore a soft-deleted patient
    Returns: (success: bool, message: str)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if patient is deleted
        cursor.execute('SELECT name FROM patients WHERE patient_id = ? AND is_deleted = 1', (patient_id,))
        patient_data = cursor.fetchone()
        
        if not patient_data:
            conn.close()
            return False, "Patient not found in deleted records"
        
        patient_name = patient_data[0]
        
        # Restore patient
        cursor.execute('UPDATE patients SET is_deleted = 0 WHERE patient_id = ?', (patient_id,))
        
        # Restore all visits
        cursor.execute('UPDATE visits SET is_deleted = 0 WHERE patient_id = ?', (patient_id,))
        restored_visits = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        # Log audit action
        log_audit_action('RESTORE', 'patients', patient_id, None, None, user_id, 
                        f"Restored patient '{patient_name}' and {restored_visits} visits")
        
        return True, f"Patient '{patient_name}' and {restored_visits} visits restored successfully"
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Error restoring patient: {str(e)}"

def get_deleted_records(limit: int = 50) -> List[Dict]:
    """
    Get list of deleted records for management
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT dr.*, 
                   CASE 
                       WHEN dr.table_name = 'patients' THEN 
                           (SELECT name FROM patients WHERE patient_id = dr.record_id)
                       ELSE 'N/A'
                   END as record_name
            FROM deleted_records dr
            ORDER BY dr.deletion_timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        deleted_records = []
        for row in results:
            deleted_records.append({
                'deletion_id': row[0],
                'table_name': row[1],
                'record_id': row[2],
                'original_data': row[3],
                'deleted_by': row[4],
                'deletion_reason': row[5],
                'deletion_timestamp': row[6],
                'can_restore': bool(row[7]),
                'record_name': row[8]
            })
        
        return deleted_records
        
    except Exception as e:
        print(f"Error getting deleted records: {str(e)}")
        return []

def get_audit_log(limit: int = 100) -> List[Dict]:
    """
    Get audit log for enterprise compliance
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM audit_log
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        audit_logs = []
        for row in results:
            audit_logs.append({
                'log_id': row[0],
                'action': row[1],
                'table_name': row[2],
                'record_id': row[3],
                'old_data': row[4],
                'new_data': row[5],
                'user_id': row[6],
                'timestamp': row[7],
                'ip_address': row[8],
                'details': row[9]
            })
        
        return audit_logs
        
    except Exception as e:
        print(f"Error getting audit log: {str(e)}")
        return []

# Update existing functions to exclude deleted records
def get_all_patients() -> List[Dict]:
    """Get all non-deleted patients"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT patient_id, name, age, gender, phone, weight, conditions, created_date
            FROM patients 
            WHERE is_deleted = 0 OR is_deleted IS NULL
            ORDER BY created_date DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        patients = []
        for row in results:
            patients.append({
                'patient_id': row[0],
                'name': row[1],
                'age': row[2],
                'gender': row[3],
                'phone': row[4],
                'weight': row[5],
                'conditions': row[6],
                'created_date': row[7],
                'created_date_formatted': format_date_for_display(row[7])
            })
        
        return patients
    
    except Exception as e:
        print(f"Error getting all patients: {str(e)}")
        return []

# Initialize database when module is imported
if __name__ == "__main__":
    success, message = init_database()
    print(message)
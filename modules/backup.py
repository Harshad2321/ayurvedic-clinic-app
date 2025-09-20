"""
Backup and Data Protection utilities for Ayurvedic Clinic Management System
Provides automatic backup, restore, and data integrity functions
"""

import os
import shutil
import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import zipfile

# Backup directory
BACKUP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backups')
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'clinic.db')

def ensure_backup_directory():
    """Create backup directory if it doesn't exist"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def create_backup(backup_type: str = "manual") -> Tuple[bool, str]:
    """
    Create a backup of the database
    Returns: (success: bool, message: str)
    """
    try:
        ensure_backup_directory()
        
        if not os.path.exists(DB_PATH):
            return False, "Database file not found"
        
        # Create timestamp for backup filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"clinic_backup_{backup_type}_{timestamp}.db"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        
        # Copy database file
        shutil.copy2(DB_PATH, backup_path)
        
        # Create metadata file
        metadata = {
            'backup_date': datetime.now().isoformat(),
            'backup_type': backup_type,
            'original_db_path': DB_PATH,
            'backup_size': os.path.getsize(backup_path),
            'app_version': '1.0.0'
        }
        
        metadata_path = backup_path.replace('.db', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Create comprehensive backup zip
        zip_path = backup_path.replace('.db', '.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(backup_path, backup_filename)
            zipf.write(metadata_path, backup_filename.replace('.db', '_metadata.json'))
        
        # Clean up individual files
        os.remove(backup_path)
        os.remove(metadata_path)
        
        # Clean old backups (keep last 10)
        cleanup_old_backups()
        
        backup_size = os.path.getsize(zip_path) / 1024  # Size in KB
        return True, f"Backup created successfully: {backup_filename.replace('.db', '.zip')} ({backup_size:.1f} KB)"
        
    except Exception as e:
        return False, f"Backup failed: {str(e)}"

def cleanup_old_backups(keep_count: int = 10):
    """Remove old backups, keeping only the most recent ones"""
    try:
        if not os.path.exists(BACKUP_DIR):
            return
        
        # Get all backup files
        backup_files = []
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith('clinic_backup_') and filename.endswith('.zip'):
                filepath = os.path.join(BACKUP_DIR, filename)
                backup_files.append((filepath, os.path.getmtime(filepath)))
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # Remove old backups
        for filepath, _ in backup_files[keep_count:]:
            os.remove(filepath)
            
    except Exception as e:
        print(f"Error cleaning up old backups: {str(e)}")

def get_backup_list() -> List[Dict]:
    """Get list of available backups"""
    try:
        ensure_backup_directory()
        backups = []
        
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith('clinic_backup_') and filename.endswith('.zip'):
                filepath = os.path.join(BACKUP_DIR, filename)
                
                # Get file info
                stat = os.stat(filepath)
                size_kb = stat.st_size / 1024
                created = datetime.fromtimestamp(stat.st_mtime)
                
                # Try to extract backup type from filename
                parts = filename.replace('clinic_backup_', '').replace('.zip', '').split('_')
                backup_type = parts[0] if parts else 'unknown'
                
                backups.append({
                    'filename': filename,
                    'filepath': filepath,
                    'backup_type': backup_type,
                    'created_date': created,
                    'created_formatted': created.strftime('%d/%m/%Y %H:%M:%S'),
                    'size_kb': size_kb,
                    'size_formatted': f"{size_kb:.1f} KB"
                })
        
        # Sort by creation date (newest first)
        backups.sort(key=lambda x: x['created_date'], reverse=True)
        return backups
        
    except Exception as e:
        print(f"Error getting backup list: {str(e)}")
        return []

def restore_backup(backup_filename: str) -> Tuple[bool, str]:
    """
    Restore database from backup
    Returns: (success: bool, message: str)
    """
    try:
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        
        if not os.path.exists(backup_path):
            return False, "Backup file not found"
        
        # Create current backup before restore
        current_backup_success, current_backup_msg = create_backup("pre_restore")
        if not current_backup_success:
            return False, f"Failed to create current backup: {current_backup_msg}"
        
        # Extract backup zip
        temp_dir = os.path.join(BACKUP_DIR, 'temp_restore')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            zipf.extractall(temp_dir)
        
        # Find the database file
        db_file = None
        for filename in os.listdir(temp_dir):
            if filename.endswith('.db'):
                db_file = os.path.join(temp_dir, filename)
                break
        
        if not db_file:
            shutil.rmtree(temp_dir)
            return False, "No database file found in backup"
        
        # Verify backup integrity
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM patients")
            patient_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM visits")
            visit_count = cursor.fetchone()[0]
            conn.close()
        except Exception as e:
            shutil.rmtree(temp_dir)
            return False, f"Backup file is corrupted: {str(e)}"
        
        # Replace current database
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        shutil.copy2(db_file, DB_PATH)
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        return True, f"Database restored successfully from {backup_filename}. Found {patient_count} patients and {visit_count} visits."
        
    except Exception as e:
        return False, f"Restore failed: {str(e)}"

def verify_database_integrity() -> Tuple[bool, List[str]]:
    """
    Verify database integrity and check for issues
    Returns: (is_healthy: bool, issues: List[str])
    """
    issues = []
    
    try:
        if not os.path.exists(DB_PATH):
            issues.append("Database file does not exist")
            return False, issues
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if main tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('patients', 'visits')
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        
        if 'patients' not in tables:
            issues.append("Patients table is missing")
        if 'visits' not in tables:
            issues.append("Visits table is missing")
        
        if issues:
            conn.close()
            return False, issues
        
        # Check for orphaned visits (visits without corresponding patients)
        cursor.execute("""
            SELECT COUNT(*) FROM visits v 
            WHERE NOT EXISTS (SELECT 1 FROM patients p WHERE p.patient_id = v.patient_id)
        """)
        orphaned_visits = cursor.fetchone()[0]
        if orphaned_visits > 0:
            issues.append(f"Found {orphaned_visits} orphaned visits (visits without corresponding patients)")
        
        # Check for duplicate phone numbers
        cursor.execute("""
            SELECT phone, COUNT(*) as count
            FROM patients 
            WHERE phone IS NOT NULL AND phone != ''
            GROUP BY phone 
            HAVING COUNT(*) > 1
        """)
        duplicate_phones = cursor.fetchall()
        if duplicate_phones:
            issues.append(f"Found {len(duplicate_phones)} duplicate phone numbers")
        
        # Check for missing required fields
        cursor.execute("""
            SELECT COUNT(*) FROM patients 
            WHERE name IS NULL OR name = '' OR age IS NULL OR gender IS NULL OR phone IS NULL OR phone = ''
        """)
        invalid_patients = cursor.fetchone()[0]
        if invalid_patients > 0:
            issues.append(f"Found {invalid_patients} patients with missing required information")
        
        # Check database size and stats
        cursor.execute("SELECT COUNT(*) FROM patients")
        patient_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM visits")
        visit_count = cursor.fetchone()[0]
        
        if patient_count == 0:
            issues.append("No patients found in database")
        
        conn.close()
        
        # Check file permissions
        if not os.access(DB_PATH, os.R_OK):
            issues.append("Cannot read database file")
        if not os.access(DB_PATH, os.W_OK):
            issues.append("Cannot write to database file")
        
        return len(issues) == 0, issues
        
    except Exception as e:
        issues.append(f"Database integrity check failed: {str(e)}")
        return False, issues

def auto_backup_if_needed() -> Tuple[bool, str]:
    """
    Create automatic backup if needed (daily or if significant changes)
    Returns: (backup_created: bool, message: str)
    """
    try:
        ensure_backup_directory()
        
        # Check if we need a backup today
        today = datetime.now().date()
        
        # Look for existing backup today
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith('clinic_backup_auto_') and filename.endswith('.zip'):
                # Extract date from filename
                try:
                    date_part = filename.split('_')[3]  # clinic_backup_auto_YYYYMMDD_HHMMSS.zip
                    backup_date = datetime.strptime(date_part, '%Y%m%d').date()
                    if backup_date == today:
                        return False, "Automatic backup already exists for today"
                except:
                    continue
        
        # Create automatic backup
        return create_backup("auto")
        
    except Exception as e:
        return False, f"Auto backup check failed: {str(e)}"

def get_database_stats() -> Dict:
    """Get comprehensive database statistics"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Basic counts
        cursor.execute("SELECT COUNT(*) FROM patients")
        patient_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM visits")
        visit_count = cursor.fetchone()[0]
        
        # Recent activity
        cursor.execute("""
            SELECT COUNT(*) FROM patients 
            WHERE created_date >= date('now', '-7 days')
        """)
        new_patients_week = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM visits 
            WHERE visit_date >= date('now', '-7 days')
        """)
        visits_week = cursor.fetchone()[0]
        
        # Database size
        db_size = os.path.getsize(DB_PATH) / 1024  # Size in KB
        
        conn.close()
        
        return {
            'patient_count': patient_count,
            'visit_count': visit_count,
            'new_patients_week': new_patients_week,
            'visits_week': visits_week,
            'db_size_kb': db_size,
            'db_size_formatted': f"{db_size:.1f} KB",
            'last_updated': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
    except Exception as e:
        return {
            'error': f"Failed to get stats: {str(e)}",
            'patient_count': 0,
            'visit_count': 0,
            'new_patients_week': 0,
            'visits_week': 0,
            'db_size_kb': 0,
            'db_size_formatted': "0 KB",
            'last_updated': 'Unknown'
        }
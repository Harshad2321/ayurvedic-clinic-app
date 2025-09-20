"""
Flask Web Application for Ayurvedic Clinic Management
Simple, fast, and easy-to-use interface for clinic management
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
import sys
import os

# Add the modules directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.database import (
    init_database, add_patient, search_patients, get_patient_by_id,
    add_visit, get_patient_visits, get_all_patients, update_patient,
    get_database_stats, get_patient_weight_progression, format_date_for_display,
    format_date_for_storage, get_today_formatted, get_patient_visit_count,
    get_patient_summary, search_patients_with_visit_info, find_existing_patient_by_phone,
    find_similar_patients, merge_patient_records, update_patient_info,
    soft_delete_patient, hard_delete_patient, soft_delete_visit, restore_deleted_patient,
    get_deleted_records, get_audit_log, log_audit_action
)

from modules.validation import (
    validate_patient_data, validate_visit_data, validate_search_term,
    sanitize_input, format_phone_number, get_validation_summary
)

from modules.backup import (
    create_backup, get_backup_list, restore_backup, verify_database_integrity,
    auto_backup_if_needed, get_database_stats as get_backup_stats
)

app = Flask(__name__)
app.secret_key = 'ayurvedic_clinic_2025'  # Change this in production

@app.route('/')
def dashboard():
    """Main dashboard with automatic backup"""
    # Check database and create backup if needed
    success, message = init_database()
    if not success:
        flash(f'Database Error: {message}', 'error')
    
    # Auto backup check
    backup_created, backup_message = auto_backup_if_needed()
    if backup_created:
        flash(f'🛡️ Automatic backup created: {backup_message}', 'info')
    
    # Get statistics
    stats = get_database_stats()
    
    # Get recent patients
    recent_patients = get_all_patients()[:5]  # Last 5 patients
    
    # Get backup status
    backup_stats = get_backup_stats()
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         recent_patients=recent_patients,
                         backup_stats=backup_stats)

from modules.backup import (
    create_backup, get_backup_list, restore_backup, verify_database_integrity,
    auto_backup_if_needed, get_database_stats as get_backup_stats
)

app = Flask(__name__)
app.secret_key = 'ayurvedic_clinic_2025'  # Change this in production

@app.route('/')
def dashboard():
    """Main dashboard"""
    # Initialize database
    success, message = init_database()
    if not success:
        flash(f'Database Error: {message}', 'error')
    
    # Get statistics
    stats = get_database_stats()
    
    # Get recent patients
    recent_patients = get_all_patients()[:5]  # Last 5 patients
    
    return render_template('dashboard.html', stats=stats, recent_patients=recent_patients)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient_route():
    """Add new patient with comprehensive validation"""
    if request.method == 'POST':
        # Get and sanitize form data
        name = sanitize_input(request.form.get('name', ''))
        age = request.form.get('age', type=int)
        gender = request.form.get('gender', '')
        phone = format_phone_number(request.form.get('phone', ''))
        weight = request.form.get('weight', type=float)
        conditions = sanitize_input(request.form.get('conditions', ''))
        registration_date = request.form.get('registration_date', '')
        
        # Comprehensive validation
        is_valid, validation_errors = validate_patient_data(name, age, gender, phone, weight, conditions)
        
        if not is_valid:
            for error in validation_errors:
                flash(f'❌ {error}', 'error')
            return render_template('add_patient.html', 
                                 today=date.today().strftime('%Y-%m-%d'),
                                 form_data={
                                     'name': name, 'age': age, 'gender': gender,
                                     'phone': phone, 'weight': weight, 'conditions': conditions
                                 })
        
        # Check for duplicates
        existing_patient = find_existing_patient_by_phone(phone)
        if existing_patient:
            flash(f'⚠️ Patient with phone {phone} already exists: {existing_patient["name"]} (ID: {existing_patient["patient_id"]})', 'warning')
            return render_template('duplicate_patient.html', 
                                 new_patient={'name': name, 'age': age, 'gender': gender, 'phone': phone, 'weight': weight, 'conditions': conditions},
                                 existing_patient=existing_patient,
                                 today=date.today().strftime('%Y-%m-%d'))
        
        # Check for similar names (potential duplicates)
        similar_patients = find_similar_patients(name, phone)
        if similar_patients:
            return render_template('similar_patients.html',
                                 new_patient={'name': name, 'age': age, 'gender': gender, 'phone': phone, 'weight': weight, 'conditions': conditions},
                                 similar_patients=similar_patients,
                                 today=date.today().strftime('%Y-%m-%d'))
        
        # Convert date format
        if not registration_date:
            registration_date = date.today().strftime('%Y-%m-%d')
        else:
            # Convert from DD/MM/YYYY to YYYY-MM-DD if needed
            try:
                reg_date_obj = datetime.strptime(registration_date, '%Y-%m-%d')
            except:
                try:
                    reg_date_obj = datetime.strptime(registration_date, '%d/%m/%Y')
                    registration_date = reg_date_obj.strftime('%Y-%m-%d')
                except:
                    registration_date = date.today().strftime('%Y-%m-%d')
        
        weight_value = weight if weight and weight > 0 else None
        conditions_value = conditions if conditions else None
        
        success, message, patient_id = add_patient(
            name, age, gender, phone, weight_value, conditions_value, registration_date
        )
        
        if success:
            flash(f'✅ {message}', 'success')
            return redirect(url_for('patient_details', patient_id=patient_id))
        else:
            flash(f'❌ {message}', 'error')
    
    return render_template('add_patient.html', today=date.today().strftime('%Y-%m-%d'))

@app.route('/force_add_patient')
def force_add_patient():
    """Force add patient when user confirms it's not a duplicate"""
    name = request.args.get('name', '').strip()
    age = request.args.get('age', type=int)
    gender = request.args.get('gender', '')
    phone = request.args.get('phone', '').strip()
    weight = request.args.get('weight', type=float)
    conditions = request.args.get('conditions', '').strip()
    
    # Validation
    if not name or not age or not gender or not phone:
        flash('Missing required information', 'error')
        return redirect(url_for('add_patient_route'))
    
    if len(phone) != 10 or not phone.isdigit():
        flash('Invalid phone number', 'error')
        return redirect(url_for('add_patient_route'))
    
    # Prepare data
    registration_date = date.today().strftime('%Y-%m-%d')
    weight_value = weight if weight and weight > 0 else None
    conditions_value = conditions if conditions else None
    
    success, message, patient_id = add_patient(
        name, age, gender, phone, weight_value, conditions_value, registration_date
    )
    
    if success:
        flash(f'✅ Patient added despite duplicate warning: {message}', 'success')
        return redirect(url_for('patient_details', patient_id=patient_id))
    else:
        flash(f'❌ {message}', 'error')
        return redirect(url_for('add_patient_route'))

@app.route('/merge_patients')
def merge_patients():
    """Merge duplicate patient records"""
    keep_id = request.args.get('keep_id', type=int)
    duplicate_id = request.args.get('duplicate_id', type=int)
    
    if not keep_id or not duplicate_id:
        flash('Invalid patient IDs for merging', 'error')
        return redirect(url_for('dashboard'))
    
    if keep_id == duplicate_id:
        flash('Cannot merge a patient with themselves', 'error')
        return redirect(url_for('dashboard'))
    
    success, message = merge_patient_records(keep_id, duplicate_id)
    
    if success:
        flash(f'✅ {message}', 'success')
        return redirect(url_for('patient_details', patient_id=keep_id))
    else:
        flash(f'❌ {message}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/search')
def search():
    """Search patients with validation"""
    search_term = sanitize_input(request.args.get('q', ''))
    patients = []
    
    if search_term:
        # Validate search term
        is_valid, validation_errors = validate_search_term(search_term)
        
        if not is_valid:
            for error in validation_errors:
                flash(f'❌ Search Error: {error}', 'error')
        else:
            patients = search_patients_with_visit_info(search_term)
    
    return render_template('search.html', patients=patients, search_term=search_term)

@app.route('/patient/<int:patient_id>')
def patient_details(patient_id):
    """Patient details and visit management"""
    summary = get_patient_summary(patient_id)
    
    if not summary:
        flash('Patient not found', 'error')
        return redirect(url_for('search'))
    
    visits = get_patient_visits(patient_id)
    weight_progression = get_patient_weight_progression(patient_id)
    
    # Get current date for the form
    from datetime import datetime
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('patient_details.html', 
                         summary=summary, 
                         visits=visits, 
                         weight_progression=weight_progression,
                         current_date=current_date)

@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    """Edit patient information"""
    patient = get_patient_by_id(patient_id)
    if not patient:
        flash('Patient not found', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Get and sanitize form data
        name = sanitize_input(request.form.get('name', ''))
        age = request.form.get('age', type=int)
        gender = request.form.get('gender', '')
        phone = format_phone_number(request.form.get('phone', ''))
        weight = request.form.get('weight', type=float)
        conditions = sanitize_input(request.form.get('conditions', ''))
        
        # Comprehensive validation
        is_valid, validation_errors = validate_patient_data(name, age, gender, phone, weight, conditions)
        
        if not is_valid:
            for error in validation_errors:
                flash(f'❌ {error}', 'error')
            return render_template('edit_patient.html', 
                                 patient=patient,
                                 form_data={
                                     'name': name, 'age': age, 'gender': gender,
                                     'phone': phone, 'weight': weight, 'conditions': conditions
                                 })
        
        # Check if phone number changed and if new phone is already taken
        if phone != patient['phone']:
            existing_patient = find_existing_patient_by_phone(phone)
            if existing_patient and existing_patient['patient_id'] != patient_id:
                flash(f'❌ Phone number {phone} is already used by another patient: {existing_patient["name"]}', 'error')
                return render_template('edit_patient.html', 
                                     patient=patient,
                                     form_data={
                                         'name': name, 'age': age, 'gender': gender,
                                         'phone': phone, 'weight': weight, 'conditions': conditions
                                     })
        
        # Update patient information
        success, message = update_patient_info(
            patient_id, name, age, gender, phone, weight, conditions
        )
        
        if success:
            flash(f'✅ {message}', 'success')
            return redirect(url_for('patient_details', patient_id=patient_id))
        else:
            flash(f'❌ {message}', 'error')
    
    return render_template('edit_patient.html', patient=patient)

@app.route('/add_visit/<int:patient_id>', methods=['POST'])
def add_visit_route(patient_id):
    """Add a new visit for a patient with validation"""
    # Get and sanitize form data
    visit_date = request.form.get('visit_date', date.today().strftime('%Y-%m-%d'))
    symptoms = sanitize_input(request.form.get('symptoms', ''))
    medicines = sanitize_input(request.form.get('medicines', ''))
    diet_notes = sanitize_input(request.form.get('diet_notes', ''))
    weight = request.form.get('weight', type=float)
    blood_pressure = sanitize_input(request.form.get('blood_pressure', ''))
    notes = sanitize_input(request.form.get('notes', ''))
    
    # Validate visit data
    is_valid, validation_errors = validate_visit_data(
        visit_date, symptoms, medicines, diet_notes, weight, blood_pressure, notes
    )
    
    if not is_valid:
        for error in validation_errors:
            flash(f'❌ {error}', 'error')
        return redirect(url_for('patient_details', patient_id=patient_id))
    
    weight_value = weight if weight and weight > 0 else None
    
    success, message = add_visit(
        patient_id, visit_date,
        symptoms if symptoms else None,
        medicines if medicines else None,
        diet_notes if diet_notes else None,
        weight_value,
        blood_pressure if blood_pressure else None,
        notes if notes else None
    )
    
    if success:
        flash(f'✅ {message}', 'success')
    else:
        flash(f'❌ {message}', 'error')
    
    return redirect(url_for('patient_details', patient_id=patient_id))

@app.route('/api/patient_info/<int:patient_id>')
def api_patient_info(patient_id):
    """API endpoint to get patient info for quick lookup"""
    summary = get_patient_summary(patient_id)
    
    if summary:
        return jsonify({
            'success': True,
            'patient': summary['patient'],
            'visit_count': summary['visit_count'],
            'is_new_patient': summary['is_new_patient'],
            'is_returning_patient': summary['is_returning_patient'],
            'last_visit_date': summary['last_visit']['visit_date_formatted'] if summary['last_visit'] else None
        })
    else:
        return jsonify({'success': False, 'message': 'Patient not found'})

@app.route('/all_patients')
def all_patients():
    """Show all patients with visit counts"""
    patients = get_all_patients()
    
    # Add visit count to each patient
    for patient in patients:
        patient['visit_count'] = get_patient_visit_count(patient['patient_id'])
        patient['is_new_patient'] = patient['visit_count'] == 0
    
    return render_template('all_patients.html', patients=patients)

# ==========================================
# ENTERPRISE DELETION AND AUDIT ROUTES
# ==========================================

@app.route('/delete_patient/<int:patient_id>')
def confirm_delete_patient(patient_id):
    """Show patient deletion confirmation page"""
    patient = get_patient_by_id(patient_id)
    if not patient:
        flash('Patient not found', 'error')
        return redirect(url_for('dashboard'))
    
    # Get visit count for confirmation
    visits = get_patient_visits(patient_id)
    visit_count = len(visits)
    
    return render_template('confirm_delete_patient.html', 
                         patient=patient, 
                         visit_count=visit_count,
                         visits=visits[:5])  # Show last 5 visits

@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
def delete_patient_route(patient_id):
    """Handle patient deletion with confirmation"""
    action = request.form.get('action')
    reason = sanitize_input(request.form.get('reason', ''))
    confirmation = request.form.get('confirmation', '')
    
    patient = get_patient_by_id(patient_id)
    if not patient:
        flash('Patient not found', 'error')
        return redirect(url_for('dashboard'))
    
    if action == 'soft_delete':
        if confirmation.lower() != 'delete':
            flash('❌ Please type "delete" to confirm deletion', 'error')
            return redirect(url_for('confirm_delete_patient', patient_id=patient_id))
        
        success, message = soft_delete_patient(patient_id, reason, 'admin')
        if success:
            flash(f'🗑️ {message}', 'warning')
            log_audit_action('SOFT_DELETE_CONFIRMED', 'patients', patient_id, 
                           None, None, 'admin', f"Reason: {reason}")
        else:
            flash(f'❌ {message}', 'error')
            
    elif action == 'hard_delete':
        confirmation_code = request.form.get('confirmation_code', '')
        expected_code = f"DELETE-{patient_id}-PERMANENT"
        
        if confirmation_code != expected_code:
            flash(f'❌ Invalid confirmation code. Required: {expected_code}', 'error')
            return redirect(url_for('confirm_delete_patient', patient_id=patient_id))
        
        success, message = hard_delete_patient(patient_id, confirmation_code, 'admin')
        if success:
            flash(f'🔥 {message}', 'warning')
        else:
            flash(f'❌ {message}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/delete_visit/<int:visit_id>')
def delete_visit_route(visit_id):
    """Delete a specific visit"""
    reason = request.args.get('reason', 'Manual deletion')
    
    success, message = soft_delete_visit(visit_id, reason, 'admin')
    if success:
        flash(f'🗑️ {message}', 'warning')
    else:
        flash(f'❌ {message}', 'error')
    
    # Redirect back to patient details if possible
    patient_id = request.args.get('patient_id')
    if patient_id:
        return redirect(url_for('patient_details', patient_id=patient_id))
    
    return redirect(url_for('dashboard'))

@app.route('/admin/deleted_records')
def admin_deleted_records():
    """Admin view of deleted records"""
    deleted_records = get_deleted_records(100)
    return render_template('admin_deleted_records.html', deleted_records=deleted_records)

@app.route('/admin/audit_log')
def admin_audit_log():
    """Admin view of audit log"""
    audit_logs = get_audit_log(200)
    return render_template('admin_audit_log.html', audit_logs=audit_logs)

@app.route('/restore_patient/<int:patient_id>', methods=['POST'])
def restore_patient_route(patient_id):
    """Restore a deleted patient"""
    success, message = restore_deleted_patient(patient_id, 'admin')
    if success:
        flash(f'♻️ {message}', 'success')
    else:
        flash(f'❌ {message}', 'error')
    
    return redirect(url_for('admin_deleted_records'))

if __name__ == '__main__':
    # Initialize database on startup
    try:
        init_database()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
    
    # Run in production mode for deployment
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
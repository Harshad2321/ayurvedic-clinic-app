"""
Ayurvedic Clinic Management System
Main Streamlit Application

A simple, user-friendly app for managing patient records and visits
Built for non-technical users with intuitive interface
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

# Add the modules directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

# Import our database module
from modules.database import (
    init_database, add_patient, search_patients, get_patient_by_id,
    add_visit, get_patient_visits, get_all_patients, update_patient,
    get_database_stats, get_patient_weight_progression, format_date_for_display,
    format_date_for_storage, get_today_formatted
)

# Page configuration
st.set_page_config(
    page_title="Ayurvedic Clinic Management",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #228B22;
        margin-bottom: 1rem;
    }
    .patient-card {
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin-bottom: 1rem;
    }
    .visit-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #dee2e6;
        margin-bottom: 0.5rem;
    }
    .date-highlight {
        background-color: #e3f2fd;
        padding: 0.3rem 0.6rem;
        border-radius: 20px;
        border: 1px solid #1976d2;
        color: #1976d2;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    .date-large {
        font-size: 1.1rem;
        color: #1976d2;
        font-weight: bold;
        background-color: #e3f2fd;
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        border: 2px solid #1976d2;
        display: inline-block;
        margin: 0.3rem 0;
    }
    .registration-date {
        background-color: #e8f5e8;
        color: #2e7d32;
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        border: 1px solid #4caf50;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem 0;
    }
    .success-message {
        color: #155724;
        background-color: #d4edda;
        padding: 0.75rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        color: #721c24;
        background-color: #f8d7da;
        padding: 0.75rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    </style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'selected_patient' not in st.session_state:
        st.session_state.selected_patient = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"

def show_dashboard():
    """Display the main dashboard"""
    st.markdown('<div class="main-header">🌿 Ayurvedic Clinic Management System</div>', unsafe_allow_html=True)
    
    # Initialize database
    success, message = init_database()
    if not success:
        st.error(f"Database Error: {message}")
        return
    
    # Get and display statistics
    stats = get_database_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Patients", stats['total_patients'])
    
    with col2:
        st.metric("Total Visits", stats['total_visits'])
    
    with col3:
        st.metric("New Patients (7 days)", stats['recent_patients'])
    
    with col4:
        st.metric("Recent Visits (7 days)", stats['recent_visits'])
    
    st.markdown("---")
    
    # Recent activity
    st.markdown('<div class="sub-header">Recent Activity</div>', unsafe_allow_html=True)
    
    # Show recent patients
    patients = get_all_patients()
    if patients:
        recent_patients = sorted(patients, key=lambda x: x['created_date'], reverse=True)[:5]
        
        st.subheader("Recently Added Patients")
        for patient in recent_patients:
            with st.container():
                st.markdown(f"""
                <div class="patient-card">
                    <strong>{patient['name']}</strong> - {patient['age']} years, {patient['gender']}<br>
                    📞 {patient['phone']}<br>
                    <div class="registration-date">📅 Registered: {patient['created_date_formatted']}</div><br>
                    Conditions: {patient['conditions'] or 'None recorded'}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No patients found. Start by adding your first patient!")

def add_new_patient():
    """Form to add a new patient"""
    st.markdown('<div class="sub-header">Add New Patient</div>', unsafe_allow_html=True)
    
    with st.form("add_patient_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Patient Name *", placeholder="Enter full name")
            age = st.number_input("Age *", min_value=0, max_value=150, value=30)
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
        
        with col2:
            phone = st.text_input("Phone Number *", placeholder="Enter 10-digit phone number")
            weight = st.number_input("Weight (kg)", min_value=0.0, value=0.0, step=0.1)
            
            # Date input with Indian format
            registration_date = st.date_input("Registration Date 📅", value=date.today(),
                                            help="Date when patient first registered")
            
        conditions = st.text_area("Medical Conditions", 
                                placeholder="Enter any existing conditions (diabetes, hypertension, etc.)")
        
        # Show formatted date preview
        formatted_date = registration_date.strftime('%d/%m/%Y')
        st.markdown(f'<div class="registration-date">📅 Registration Date: {formatted_date}</div>', 
                   unsafe_allow_html=True)
        
        submitted = st.form_submit_button("Add Patient", type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            if not name.strip():
                st.error("Patient name is required")
                return
            
            if not phone.strip():
                st.error("Phone number is required")
                return
            
            if len(phone.strip()) != 10 or not phone.strip().isdigit():
                st.error("Please enter a valid 10-digit phone number")
                return
            
            # Add patient to database
            weight_value = weight if weight > 0 else None
            conditions_value = conditions.strip() if conditions.strip() else None
            reg_date = registration_date.strftime('%Y-%m-%d')  # Store in database format
            
            success, message, patient_id = add_patient(
                name.strip(), age, gender, phone.strip(), weight_value, conditions_value, reg_date
            )
            
            if success:
                st.success(f"✅ {message}")
                st.balloons()
                # Reset form by rerunning
                st.rerun()
            else:
                st.error(f"❌ {message}")

def search_and_select_patient():
    """Search for patients and select one"""
    st.markdown('<div class="sub-header">Search Patients</div>', unsafe_allow_html=True)
    
    search_term = st.text_input("Search by name or phone number", 
                               placeholder="Enter patient name or phone number")
    
    if search_term:
        patients = search_patients(search_term)
        
        if patients:
            st.success(f"Found {len(patients)} patient(s)")
            
            for patient in patients:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div class="patient-card">
                            <strong>{patient['name']}</strong><br>
                            Age: {patient['age']} | Gender: {patient['gender']}<br>
                            📞 {patient['phone']}<br>
                            Weight: {patient['weight'] or 'Not recorded'} kg<br>
                            Conditions: {patient['conditions'] or 'None recorded'}<br>
                            <div class="registration-date">📅 Registered: {patient['created_date_formatted']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        if st.button(f"Select", key=f"select_{patient['patient_id']}", 
                                   type="primary", use_container_width=True):
                            st.session_state.selected_patient = patient
                            st.session_state.current_page = "Patient Details"
                            st.rerun()
        else:
            st.warning("No patients found matching your search")
    
    # Show all patients option
    if st.checkbox("Show all patients"):
        all_patients = get_all_patients()
        if all_patients:
            st.info(f"Total patients: {len(all_patients)}")
            
            # Create a more compact view for all patients
            df = pd.DataFrame(all_patients)
            df = df[['name', 'age', 'gender', 'phone', 'conditions']]
            
            # Add selection
            selected_indices = st.multiselect(
                "Select a patient to view details:",
                range(len(df)),
                format_func=lambda x: f"{df.iloc[x]['name']} - {df.iloc[x]['phone']}"
            )
            
            if selected_indices:
                idx = selected_indices[0]  # Take first selection
                selected_patient = all_patients[idx]
                st.session_state.selected_patient = selected_patient
                st.session_state.current_page = "Patient Details"
                st.rerun()

def show_patient_details():
    """Show detailed view of selected patient"""
    if not st.session_state.selected_patient:
        st.warning("No patient selected. Please search and select a patient first.")
        return
    
    patient = st.session_state.selected_patient
    
    # Patient header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="sub-header">Patient Details: {patient["name"]}</div>', unsafe_allow_html=True)
    with col2:
        if st.button("Back to Search", type="secondary"):
            st.session_state.current_page = "Search Patients"
            st.rerun()
    
    # Patient info card
    st.markdown(f"""
    <div class="patient-card">
        <h4>{patient['name']}</h4>
        <strong>Age:</strong> {patient['age']} years<br>
        <strong>Gender:</strong> {patient['gender']}<br>
        <strong>Phone:</strong> {patient['phone']}<br>
        <strong>Current Weight:</strong> {patient['weight'] or 'Not recorded'} kg<br>
        <strong>Conditions:</strong> {patient['conditions'] or 'None recorded'}<br>
        <div class="registration-date">📅 Registration: {patient['created_date_formatted']}</div><br>
        <strong>Patient ID:</strong> #{patient['patient_id']}
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Add Visit", "Visit History", "Weight Progress", "Update Patient"])
    
    with tab1:
        add_visit_form(patient['patient_id'])
    
    with tab2:
        show_visit_history(patient['patient_id'])
    
    with tab3:
        show_weight_progress(patient['patient_id'])
    
    with tab4:
        update_patient_form(patient)

def add_visit_form(patient_id):
    """Form to add a new visit for a patient"""
    st.subheader("Add New Visit")
    
    with st.form("add_visit_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            visit_date = st.date_input("Visit Date 📅", value=date.today(),
                                     help="Date of this visit")
            symptoms = st.text_area("Symptoms", placeholder="Describe patient's symptoms")
            medicines = st.text_area("Medicines Prescribed", placeholder="List medicines and dosage")
        
        with col2:
            diet_notes = st.text_area("Diet Recommendations", placeholder="Diet and lifestyle advice")
            weight = st.number_input("Current Weight (kg)", min_value=0.0, value=0.0, step=0.1)
            blood_pressure = st.text_input("Blood Pressure", placeholder="e.g., 120/80")
        
        notes = st.text_area("Additional Notes", placeholder="Any other observations or instructions")
        
        # Show formatted date preview
        formatted_visit_date = visit_date.strftime('%d/%m/%Y')
        st.markdown(f'<div class="date-large">📅 Visit Date: {formatted_visit_date}</div>', 
                   unsafe_allow_html=True)
        
        submitted = st.form_submit_button("Add Visit", type="primary", use_container_width=True)
        
        if submitted:
            weight_value = weight if weight > 0 else None
            
            success, message = add_visit(
                patient_id, visit_date.strftime('%Y-%m-%d'),  # Store in database format
                symptoms.strip() if symptoms.strip() else None,
                medicines.strip() if medicines.strip() else None,
                diet_notes.strip() if diet_notes.strip() else None,
                weight_value,
                blood_pressure.strip() if blood_pressure.strip() else None,
                notes.strip() if notes.strip() else None
            )
            
            if success:
                st.success(f"✅ {message}")
                st.rerun()
            else:
                st.error(f"❌ {message}")

def show_visit_history(patient_id):
    """Display visit history for a patient"""
    st.subheader("Visit History")
    
    visits = get_patient_visits(patient_id)
    
    if visits:
        st.info(f"Total visits: {len(visits)}")
        
        # Show summary stats
        col1, col2, col3 = st.columns(3)
        with col1:
            first_visit = visits[-1]['visit_date_formatted'] if visits else "N/A"
            st.metric("First Visit", first_visit)
        with col2:
            last_visit = visits[0]['visit_date_formatted'] if visits else "N/A"
            st.metric("Last Visit", last_visit)
        with col3:
            weights_recorded = len([v for v in visits if v['weight']])
            st.metric("Weights Recorded", weights_recorded)
        
        st.markdown("---")
        
        for i, visit in enumerate(visits):
            visit_number = len(visits) - i
            is_return_visit = i < len(visits) - 1
            
            with st.expander(
                f"{'🔄 Return ' if is_return_visit else '🆕 First '}Visit #{visit_number} - {visit['visit_date_formatted']}", 
                expanded=(i==0)
            ):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f'<div class="date-highlight">📅 {visit["visit_date_formatted"]}</div>', 
                               unsafe_allow_html=True)
                    if visit['symptoms']:
                        st.write(f"**🩺 Symptoms:** {visit['symptoms']}")
                    if visit['medicines']:
                        st.write(f"**💊 Medicines:** {visit['medicines']}")
                
                with col2:
                    if visit['weight']:
                        # Show weight change if it's a return visit
                        weight_text = f"{visit['weight']} kg"
                        if i < len(visits) - 1:  # Not the first visit
                            prev_weight = None
                            for j in range(i + 1, len(visits)):
                                if visits[j]['weight']:
                                    prev_weight = visits[j]['weight']
                                    break
                            if prev_weight:
                                change = visit['weight'] - prev_weight
                                if change > 0:
                                    weight_text += f" (+{change:.1f} kg ⬆️)"
                                elif change < 0:
                                    weight_text += f" ({change:.1f} kg ⬇️)"
                                else:
                                    weight_text += " (No change ➡️)"
                        st.write(f"**⚖️ Weight:** {weight_text}")
                    
                    if visit['blood_pressure']:
                        st.write(f"**🩸 Blood Pressure:** {visit['blood_pressure']}")
                    if visit['diet_notes']:
                        st.write(f"**🥗 Diet Notes:** {visit['diet_notes']}")
                
                if visit['notes']:
                    st.write(f"**📝 Additional Notes:** {visit['notes']}")
                
                # Show time since last visit for return visits
                if i < len(visits) - 1:
                    current_date = datetime.strptime(visit['visit_date'], '%Y-%m-%d')
                    prev_date = datetime.strptime(visits[i + 1]['visit_date'], '%Y-%m-%d')
                    days_between = (current_date - prev_date).days
                    st.caption(f"⏱️ {days_between} days since previous visit")
    else:
        st.info("No visits recorded yet. Add the first visit above.")

def show_weight_progress(patient_id):
    """Display weight progression for a patient"""
    st.subheader("Weight Progress")
    
    weight_records = get_patient_weight_progression(patient_id)
    
    if weight_records:
        st.info(f"Total weight records: {len(weight_records)}")
        
        # Create a DataFrame for better display
        df = pd.DataFrame(weight_records)
        
        # Display as a chart if we have multiple records
        if len(weight_records) > 1:
            st.subheader("Weight Trend Chart")
            df['date'] = pd.to_datetime(df['date'])
            st.line_chart(data=df.set_index('date')['weight'])
        
        # Display detailed records
        st.subheader("Weight Records")
        for i, record in enumerate(weight_records):
            weight_change = ""
            if i > 0:
                prev_weight = weight_records[i-1]['weight']
                change = record['weight'] - prev_weight
                if change > 0:
                    weight_change = f"(+{change:.1f} kg ⬆️)"
                elif change < 0:
                    weight_change = f"({change:.1f} kg ⬇️)"
                else:
                    weight_change = "(No change ➡️)"
            
            with st.container():
                col1, col2, col3 = st.columns([2, 2, 2])
                with col1:
                    st.write(f"**{record['date']}**")
                with col2:
                    st.write(f"**{record['weight']} kg** {weight_change}")
                with col3:
                    st.write(f"*{record['type']}*")
    else:
        st.info("No weight records found. Weight tracking will start when you add visits with weight measurements.")

def update_patient_form(patient):
    """Form to update patient information"""
    st.subheader("Update Patient Information")
    
    with st.form("update_patient_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Patient Name", value=patient['name'])
            age = st.number_input("Age", min_value=0, max_value=150, value=patient['age'])
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                                index=["Male", "Female", "Other"].index(patient['gender']))
        
        with col2:
            phone = st.text_input("Phone Number", value=patient['phone'])
            weight = st.number_input("Weight (kg)", min_value=0.0, 
                                   value=float(patient['weight']) if patient['weight'] else 0.0, 
                                   step=0.1)
        
        conditions = st.text_area("Medical Conditions", value=patient['conditions'] or "")
        
        submitted = st.form_submit_button("Update Patient", type="primary", use_container_width=True)
        
        if submitted:
            weight_value = weight if weight > 0 else None
            conditions_value = conditions.strip() if conditions.strip() else None
            
            success, message = update_patient(
                patient['patient_id'], name.strip(), age, gender, 
                phone.strip(), weight_value, conditions_value
            )
            
            if success:
                st.success(f"✅ {message}")
                # Update session state
                st.session_state.selected_patient.update({
                    'name': name.strip(),
                    'age': age,
                    'gender': gender,
                    'phone': phone.strip(),
                    'weight': weight_value,
                    'conditions': conditions_value
                })
                st.rerun()
            else:
                st.error(f"❌ {message}")

def main():
    """Main application function"""
    init_session_state()
    
    # Sidebar navigation
    st.sidebar.image("https://via.placeholder.com/200x100/2E8B57/FFFFFF?text=Ayurvedic+Clinic", 
                     caption="Clinic Management System")
    
    st.sidebar.markdown("---")
    
    # Navigation menu
    menu_options = ["Dashboard", "Add New Patient", "Search Patients", "Patient Details"]
    
    if st.session_state.current_page not in menu_options:
        st.session_state.current_page = "Dashboard"
    
    selected_page = st.sidebar.selectbox(
        "Navigation",
        menu_options,
        index=menu_options.index(st.session_state.current_page)
    )
    
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        st.rerun()
    
    # Quick stats in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Quick Stats")
    stats = get_database_stats()
    st.sidebar.metric("Total Patients", stats['total_patients'])
    st.sidebar.metric("Total Visits", stats['total_visits'])
    
    # Main content area
    if st.session_state.current_page == "Dashboard":
        show_dashboard()
    elif st.session_state.current_page == "Add New Patient":
        add_new_patient()
    elif st.session_state.current_page == "Search Patients":
        search_and_select_patient()
    elif st.session_state.current_page == "Patient Details":
        show_patient_details()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "🌿 Ayurvedic Clinic Management System | Built with ❤️ for better patient care"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
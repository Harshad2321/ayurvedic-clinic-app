# Ayurvedic Clinic Management System

A simple, user-friendly application for managing patient records and visits in an Ayurvedic clinic. Built specifically for non-technical users with an intuitive interface.

## Features (Phase 1)

✅ **Patient Management**
- Add new patients with complete information
- Search patients by name or phone number
- Update patient information
- View patient statistics

✅ **Visit Tracking**
- Record patient visits with symptoms, medicines, and diet notes
- Auto-date stamping for visits
- Track weight and blood pressure over time
- Add detailed notes for each visit

✅ **Patient History**
- View complete visit history for each patient
- Timeline view of all past visits
- Easy navigation through patient records

✅ **Dashboard**
- Overview of total patients and visits
- Recent activity tracking
- Quick statistics display

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step-by-Step Installation

1. **Open Command Prompt (PowerShell)**
   - Press `Win + R`, type `powershell`, and press Enter

2. **Navigate to the project folder**
   ```powershell
   cd c:\Users\harsh\clinic
   ```

3. **Install required packages**
   ```powershell
   pip install streamlit pandas
   ```

4. **Run the application**
   ```powershell
   streamlit run app.py
   ```

5. **Access the application**
   - The app will automatically open in your web browser
   - If not, go to: http://localhost:8501

### Alternative Installation (if pip doesn't work)

If you encounter issues with pip, try:

```powershell
python -m pip install streamlit pandas
```

Or install Python from Microsoft Store and then install packages.

## How to Use the Application

### 1. Starting the App
- Run the command: `streamlit run app.py`
- The app opens in your web browser
- Use the sidebar to navigate between different sections

### 2. Adding a New Patient
- Click "Add New Patient" in the sidebar
- Fill in the required fields:
  - Patient Name (required)
  - Age (required)
  - Gender (required)
  - Phone Number (required, 10 digits)
  - Weight (optional)
  - Medical Conditions (optional)
- Click "Add Patient" to save

### 3. Searching for Patients
- Click "Search Patients" in the sidebar
- Type patient name or phone number in the search box
- Click "Select" next to the patient you want to view
- Use "Show all patients" checkbox to see everyone

### 4. Recording a Visit
- After selecting a patient, go to "Patient Details"
- Click the "Add Visit" tab
- Fill in visit information:
  - Visit Date (auto-set to today)
  - Symptoms
  - Medicines Prescribed
  - Diet Recommendations
  - Current Weight
  - Blood Pressure
  - Additional Notes
- Click "Add Visit" to save

### 5. Viewing Patient History
- In "Patient Details", click the "Visit History" tab
- See all past visits in chronological order
- Click on any visit to expand and see full details

### 6. Updating Patient Information
- In "Patient Details", click the "Update Patient" tab
- Modify any patient information
- Click "Update Patient" to save changes

## File Structure

```
clinic/
├── app.py                 # Main Streamlit application
├── modules/
│   └── database.py        # Database operations
├── data/
│   └── clinic.db         # SQLite database (created automatically)
├── assets/               # For future images/files
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Database Information

The app uses SQLite database with two main tables:

**Patients Table:**
- patient_id (auto-generated)
- name, age, gender, phone
- weight, conditions
- created_date, updated_date

**Visits Table:**
- visit_id (auto-generated)
- patient_id (links to patient)
- visit_date, symptoms, medicines
- diet_notes, weight, blood_pressure
- notes, created_timestamp

## Troubleshooting

### Common Issues

1. **"streamlit: command not found"**
   - Make sure Python and pip are installed
   - Try: `python -m streamlit run app.py`

2. **"ModuleNotFoundError: No module named 'streamlit'"**
   - Install Streamlit: `pip install streamlit`

3. **Database errors**
   - The database is created automatically
   - Check if you have write permissions in the folder

4. **Port already in use**
   - Stop other Streamlit apps or use: `streamlit run app.py --server.port 8502`

### Getting Help

If you encounter any issues:
1. Check that all files are in the correct locations
2. Verify Python and packages are installed correctly
3. Make sure you're running the command from the clinic folder
4. Check the terminal for specific error messages

## Future Phases (Coming Soon)

🔄 **Phase 2: Rule-Based Suggestions**
- Automatic diet and lifestyle recommendations
- Condition-based advice system

🔄 **Phase 3: AI Assistant**
- Smart recommendations using AI
- Natural language queries
- Patient history analysis

🔄 **Phase 4: Advanced Features**
- PDF report generation
- Progress graphs and charts
- Voice input/output support
- Hindi language support

## Data Security

- All data is stored locally on your computer
- No internet connection required for basic functionality
- Regular backups of the database are recommended
- Patient data remains private and secure

---

**Built with ❤️ for better patient care**

For technical support or feature requests, please contact the developer.
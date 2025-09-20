# Quick Start Guide - Ayurvedic Clinic App

## 🚀 How to Start the App

1. **Open PowerShell**
   - Press `Windows Key + R`
   - Type `powershell` and press Enter

2. **Go to the clinic folder**
   ```
   cd c:\Users\harsh\clinic
   ```

3. **Activate the virtual environment**
   ```
   .\venv\Scripts\Activate.ps1
   ```

4. **Start the app**
   ```
   python -m streamlit run app.py
   ```

5. **Open your web browser**
   - Go to: http://localhost:8501
   - The app will open automatically

## 📱 How to Use the App

### Adding a New Patient
1. Click "Add New Patient" in the sidebar
2. Fill in the patient details:
   - Name (required)
   - Age (required) 
   - Gender (required)
   - Phone number (required - 10 digits)
   - Weight (optional)
   - Medical conditions (optional)
3. Click "Add Patient"

### Finding a Patient
1. Click "Search Patients" in the sidebar
2. Type the patient's name or phone number
3. Click "Select" next to the patient you want

### Adding a New Patient
1. Click "Add New Patient" in the sidebar
2. Fill in the patient details:
   - Name (required)
   - Age (required) 
   - Gender (required)
   - Phone number (required - 10 digits)
   - Weight (optional)
   - Registration Date (auto-set to today, displayed as DD/MM/YYYY)
   - Medical conditions (optional)
3. The registration date will be shown in Indian format (DD/MM/YYYY)
4. Click "Add Patient"

### Recording a Return Visit
1. First, find and select a patient
2. Go to "Patient Details"
3. Click the "Add Visit" tab
4. Fill in visit details:
   - Visit Date (auto-set to today, shown as DD/MM/YYYY)
   - New weight (if changed)
   - Current symptoms
   - Medicines prescribed
   - Diet recommendations
   - Blood pressure
   - Any additional notes
5. All dates are displayed in DD/MM/YYYY format for easy reading
6. Click "Add Visit"

### Viewing Patient History
1. Select a patient
2. Go to "Patient Details"
3. Use the tabs to see:
   - **Visit History**: All past visits with return visit indicators
   - **Weight Progress**: Weight tracking chart and progression
4. The history shows:
   - Whether each visit was a first visit or return visit
   - Weight changes between visits
   - Days between visits for return patients

## 🛑 How to Stop the App

- In PowerShell, press `Ctrl + C`
- Close the browser tab
- Close PowerShell

## 📞 Need Help?

- Make sure all information is filled correctly
- Phone numbers must be exactly 10 digits
- Patient names are required
- If something doesn't work, restart the app

---
**Remember: The app saves everything automatically. Your patient data is safe on your computer!**
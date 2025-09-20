# Quick Start Guide - Ayurvedic Clinic App (Flask Version)

## 🚀 How to Start the App

### Super Easy Method (For Your Mom):
1. **Double-click** `start_flask_app.bat` file
2. Wait for the app to start (shows "Running on http://127.0.0.1:5000")
3. **Open your web browser** and go to: http://127.0.0.1:5000
4. The clinic app will load automatically!

### Manual Method:
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
   python flask_app.py
   ```

5. **Open your web browser**
   - Go to: http://127.0.0.1:5000

## 📱 How to Use the App

### Adding a New Patient
1. Click "Add Patient" in the navigation bar
2. Fill in the patient details:
   - Name (required)
   - Age (required) 
   - Gender (required)
   - Phone number (required - 10 digits)
   - Weight (optional)
   - Registration Date (auto-set to today, shown as DD/MM/YYYY)
   - Medical conditions (optional)
3. Click "Add Patient"
4. You'll be taken to the patient details page

### Finding a Patient
1. Click "Search Patients" in the navigation bar
2. Type the patient's name or phone number
3. Click "Search" 
4. **You'll see visit count information:**
   - 🌟 "New Patient" badge for patients who haven't visited yet
   - 📊 "X visits" badge for returning patients
5. Click "Select Patient" to view details

### When Patient Returns - Visit Count Display
**This is the key feature you requested!**

When you search for a patient who has visited before, you'll see:
- **"X visits recorded"** badge showing total visits
- **"Returning Patient"** status
- **Clear indication** this is not their first visit

### Recording a Visit
1. After selecting a patient, you'll see their details page
2. **Important**: The page shows if this is a:
   - ✨ **"New Patient (No visits yet)"** - First time visitor
   - 🔄 **"Returning Patient: X visits before"** - Has visited X times
3. Fill in the visit form:
   - Visit Date (auto-set to today)
   - Symptoms, medicines, diet recommendations
   - Current weight, blood pressure
   - Additional notes
4. Click "Record First Visit" or "Add Visit #X" (depending on visit count)

### Viewing Patient History
- All past visits are shown below the form
- Each visit is numbered (Visit #1, Visit #2, etc.)
- First visit is marked with a ⭐ star
- Return visits are marked with 🔄 arrows

## 🛑 How to Stop the App

- In PowerShell, press `Ctrl + C`
- Close the browser tab
- Close PowerShell

## 💡 Key Features for Your Mom

### Visit Count Tracking
- **Always shows** how many times a patient has visited
- **Clear indicators** for new vs returning patients
- **No confusion** about patient history

### Easy Interface
- **No page refreshes** needed (faster than Streamlit)
- **Bootstrap design** - professional and clean
- **Large buttons** and clear labels
- **Color-coded badges** for quick recognition

### Patient Status Display
When you select any patient, you immediately see:
```
🌟 New Patient (No visits yet)
```
OR
```
🔄 Returning Patient: 3 visits recorded
Last visit was on 20/09/2025
```

## 📞 Need Help?

- Make sure all required information is filled correctly
- Phone numbers must be exactly 10 digits
- Patient names are required
- If something doesn't work, restart the app using the .bat file

---
**Remember: The app automatically tracks visit counts. You'll always know if a patient is new or returning!**
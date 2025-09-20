# 🏥 Ayurvedic Clinic Management System

A comprehensive, enterprise-grade clinic management application for Ayurvedic practices. Features secure authentication, professional patient management, and integrated health education.

## 🌟 Key Features

### 🔐 **Secure Authentication**
- Mobile-based login system (9898143702)
- PIN verification for clinic access
- Session management with automatic logout
- Public clinic information page

### 👥 **Patient Management**
- Complete patient registration with validation
- Advanced search and filtering capabilities
- Comprehensive patient profiles
- Mobile-optimized interface

### 📋 **Visit Tracking & Records**
- Detailed visit documentation
- Symptoms, diagnosis, and treatment tracking
- Medicine prescriptions and dosage
- Diet recommendations and lifestyle advice
- Weight and vital signs monitoring

### 🗃️ **Enterprise Data Management**
- Soft deletion with audit trails
- Data recovery capabilities
- Administrative oversight controls
- Database backup and statistics

### 📚 **Health Education System**
- Daily rotating health facts
- 15+ Ayurvedic wellness tips
- Seasonal health recommendations
- Professional health guidance

### 🎨 **Professional Interface**
- Dr. Harsh's Ayurvedic Clinic branding
- Responsive Bootstrap 5 design
- Mobile-first accessibility
- Professional clinic information display

## 🚀 Live Application

**URL:** https://ayurvedic-clinic-app.onrender.com

### 🔑 Access Credentials
- **Mobile:** 9898143702
- **PIN:** Contact clinic administrator

### 📱 Public Pages
- **Clinic Information:** https://ayurvedic-clinic-app.onrender.com/clinic-info
- **Health Tips:** Automatically displayed throughout the app

## 🛠️ Local Development

### Prerequisites
- Python 3.8+
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/Harshad2321/ayurvedic-clinic-app.git
cd ayurvedic-clinic-app

# Install dependencies
pip install -r requirements.txt

# Run the application
python flask_app.py
```

### Development Server
```
http://localhost:5000
```

## 🏗️ Technical Architecture

### Backend
- **Framework:** Flask 3.0.0
- **Database:** SQLite with enterprise features
- **Authentication:** Session-based with mobile verification
- **Security:** Form validation, SQL injection protection

### Frontend
- **UI Framework:** Bootstrap 5.3.0
- **Icons:** Bootstrap Icons + Font Awesome
- **Responsive:** Mobile-first design
- **Accessibility:** ARIA labels, keyboard navigation

### Cloud Infrastructure
- **Platform:** Render.com
- **Deployment:** Auto-deploy from GitHub
- **Domain:** Custom subdomain with SSL
- **Monitoring:** Health check endpoints

## 📊 Database Schema

### Core Tables
- **patients:** Patient information and demographics
- **visits:** Visit records with medical details
- **audit_log:** Enterprise audit trail
- **deleted_records:** Soft deletion tracking

### Features
- Foreign key constraints
- Audit trail logging
- Soft deletion capabilities
- Data integrity validation

## 🔧 Configuration

### Environment Variables
```python
# Development
DEBUG = True
SECRET_KEY = 'development-key'

# Production (auto-configured on Render)
DEBUG = False
SECRET_KEY = 'production-key'
```

### Authentication Settings
- Mobile verification: 9898143702
- PIN requirement: 4-6 digits
- Session timeout: Browser session
- Failed login protection: Built-in

## 📁 Project Structure

```
ayurvedic-clinic-app/
├── flask_app.py              # Main application
├── database.py               # Database operations
├── requirements.txt          # Python dependencies
├── Procfile                  # Render deployment config
├── render.yaml              # Render service configuration
├── modules/
│   ├── auth.py              # Authentication system
│   ├── health_facts.py      # Health education content
│   └── enterprise_deletion.py # Enterprise deletion features
├── templates/
│   ├── base.html            # Base template with branding
│   ├── login.html           # Secure login page
│   ├── dashboard.html       # Main dashboard
│   ├── clinic_info.html     # Public clinic information
│   └── [other templates]   # Feature-specific pages
└── static/
    └── [CSS/JS files]       # Static assets
```

## 🚀 Deployment

### Automatic Deployment
- **Trigger:** Push to main branch
- **Platform:** Render.com
- **Build:** Automatic dependency installation
- **Health Check:** `/health` endpoint

### Manual Deployment
```bash
# Commit changes
git add .
git commit -m "Update description"
git push

# Render automatically deploys
```

## 🔒 Security Features

### Authentication
- Mobile number verification
- PIN-based access control
- Session management
- Login attempt monitoring

### Data Protection
- SQL injection prevention
- XSS protection
- CSRF token validation
- Secure session handling

### Access Control
- Role-based permissions
- Admin-only functions
- Public information pages
- Secure logout

## 📈 Enterprise Features

### Audit & Compliance
- Complete audit trail logging
- Soft deletion with recovery
- Data modification tracking
- Administrative oversight

### Performance
- Optimized database queries
- Efficient data loading
- Mobile-responsive design
- Cloud-optimized deployment

### Scalability
- Modular architecture
- Microservice-ready design
- Database optimization
- Cloud-native deployment

## 🎯 Professional Customization

### Clinic Branding
- **Doctor:** Dr. [Name]
- **Specialization:** Ayurvedic Medicine
- **Experience:** [Years] years
- **Qualifications:** [Degrees/Certifications]

### Services Offered
- Traditional Ayurvedic consultation
- Pulse diagnosis and treatment
- Herbal medicine prescriptions
- Panchakarma therapies
- Lifestyle and dietary guidance

### Health Education
- Daily rotating wellness tips
- Seasonal health recommendations
- Ayurvedic lifestyle guidance
- Natural healing principles

## 📞 Support & Contact

### Technical Support
- **GitHub Issues:** [Repository Issues](https://github.com/Harshad2321/ayurvedic-clinic-app/issues)
- **Documentation:** This README file
- **Code Comments:** Comprehensive inline documentation

### Clinic Information
- **Phone:** [Contact Number]
- **Email:** [Contact Email]
- **Address:** [Clinic Address]
- **Hours:** [Operating Hours]

## 📝 License & Credits

### Open Source
- **License:** MIT License
- **Framework:** Flask (BSD License)
- **UI:** Bootstrap (MIT License)
- **Icons:** Font Awesome (Free License)

### Development
- **Built with:** ❤️ for better patient care
- **Designed for:** Modern Ayurvedic practices
- **Optimized for:** Mobile and desktop use

---

**🌿 Committed to Natural Healing & Wellness | Dr. Harsh's Ayurvedic Clinic 2025**
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
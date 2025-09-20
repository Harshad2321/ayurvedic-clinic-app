# 🔒 Security & Privacy Configuration

## Overview
This document explains how sensitive information is handled securely in the Ayurvedic Clinic Management System.

## 🔐 Environment Variables (Production)

For production deployment on Render.com, set these environment variables in the Render dashboard:

### Required Environment Variables:
```
CLINIC_MOBILE=9898143702
CLINIC_PIN=1978
SECRET_KEY=your_super_secure_secret_key_here
SUPPORT_NAME=Harshad Agrawal
SUPPORT_PHONE=7622871384
SUPPORT_EMAIL=harshadd.agrawal2005@gmail.com
DOCTOR_NAME=Dr. Mom's Name
CLINIC_NAME=Dr. Harsh's Ayurvedic Clinic
CLINIC_ADDRESS=Your Clinic Address, City, State - 123456
CLINIC_EMAIL=clinic@ayurveda.com
FLASK_ENV=production
```

## 🔒 Files Never Committed to GitHub

The following files contain sensitive information and are automatically excluded from GitHub:

### Sensitive Files (in .gitignore):
- `.env` - Local environment variables
- `*.db` - Database files with patient data
- `*.sqlite*` - SQLite database files
- `config_private.py` - Private configuration files
- `secrets.py` - Any secrets/credentials
- `credentials.json` - Authentication files

## 🛡️ Security Features

### 1. Environment Variable Protection
- All sensitive data stored in environment variables
- Local `.env` file for development (never committed)
- Production variables set in Render dashboard
- Fallback values for development only

### 2. Configuration Classes
- `config.py` handles secure configuration
- Separate development and production configs
- Validation of required environment variables
- Secure credential management

### 3. Authentication Security
- Mobile number and PIN stored as environment variables
- No hardcoded credentials in source code
- Session-based authentication
- Secure session management

## 🚀 Deployment Setup

### On Render.com:
1. Go to your service dashboard
2. Navigate to "Environment" tab
3. Add all required environment variables listed above
4. Deploy - the app will use these secure values

### Local Development:
1. Copy `.env.example` to `.env`
2. Fill in your actual values in `.env`
3. The `.env` file stays on your computer only

## 🔍 Verification

The system automatically validates that all required environment variables are present in production mode. If any are missing, the app will show an error.

## 📱 What's Protected:

- ✅ Login credentials (mobile & PIN)
- ✅ Flask secret key
- ✅ Personal contact information
- ✅ Clinic details and addresses
- ✅ Database files with patient data
- ✅ Any private configuration files

## 🌐 What's Public:

- ✅ Source code structure
- ✅ HTML templates (without sensitive data)
- ✅ General application logic
- ✅ Dependencies and requirements
- ✅ Documentation

This ensures your privacy while keeping the code open source! 🎉
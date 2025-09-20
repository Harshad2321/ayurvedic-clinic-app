@echo off
echo 🏥 Ayurvedic Clinic App - Cloud Deployment
echo =========================================

REM Check if git is initialized
if not exist ".git" (
    echo 📦 Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit - Ayurvedic Clinic Management System"
)

echo.
echo 🌐 DEPLOYMENT OPTIONS:
echo.
echo 1. 🎯 RENDER.COM (Recommended)
echo    - Go to: https://render.com
echo    - Connect GitHub and deploy this repo
echo    - Build Command: pip install -r requirements.txt && python -c "from modules.database import init_database; init_database()"
echo    - Start Command: gunicorn --bind 0.0.0.0:$PORT flask_app:app
echo.
echo 2. 🚄 RAILWAY.APP (Fastest)
echo    - Go to: https://railway.app
echo    - Deploy from GitHub repo
echo    - Auto-deploys in 2 minutes!
echo.
echo 3. ⚡ VERCEL (Instant)
echo    - Go to: https://vercel.com
echo    - Import GitHub repository
echo    - Instant deployment!
echo.

echo 📋 DEPLOYMENT FILES READY:
echo ✅ requirements.txt
echo ✅ Procfile
echo ✅ render.yaml
echo ✅ Flask app configured for production
echo.

echo 🎉 Your clinic app is ready for cloud deployment!
echo 📱 After deployment, your mom can access it from any phone/computer!
echo.
echo 📖 See DEPLOYMENT_GUIDE.md for detailed instructions

pause
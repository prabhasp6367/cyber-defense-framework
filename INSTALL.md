# INSTALLATION GUIDE - AI Cyber Defense Framework

## ⚡ Fast Installation (3-5 minutes)

### Option 1: Automated Setup (Recommended)

**Linux/Mac:**
```bash
cd cyber-defense-framework
chmod +x start.sh
./start.sh
```

**Windows:**
```cmd
cd cyber-defense-framework
start.bat
```

### Option 2: Manual Setup

**1. Clone Repository**
```bash
git clone https://github.com/prabhasp6367/cyber-defense-framework.git
cd cyber-defense-framework
```

**2. Create Virtual Environment**
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Initialize Database**
```bash
python setup.py
```

**5. Run Application**
```bash
python app.py
```

## 🌐 Access Application

- **URL:** http://localhost:5000
- **Username:** admin
- **Password:** password123

## 📊 Quick Demo

### 1. View Dashboard
- Navigate to http://localhost:5000/dashboard
- See live threat statistics
- View threat timeline charts

### 2. Upload Sample Logs
- Go to Security Logs page
- Upload `data/sample_logs.csv`
- AI automatically analyzes logs

### 3. View Detected Threats
- Check Alerts page
- See AI-detected suspicious activities
- Review risk scores and severity

### 4. Create Incident
- Navigate to Incidents
- Click "New Incident"
- Assign and track investigation

### 5. Simulate Response
- Go to Response Center
- Select response action
- Execute simulated response

## 🧪 Test AI Detection

```bash
# Test threat detection in Python
python3 -c "
from backend.services.threat_detector import ThreatDetector
detector = ThreatDetector()

# Normal activity
features = {'login_attempts': 1, 'failed_logins': 0, 'bytes_transferred': 50000, 'packets': 100, 'source_port': 5432, 'destination_port': 443}
pred, conf, threat, score = detector.predict(features)
print(f'Normal: Risk Score = {score:.1f}')

# Suspicious activity
features = {'login_attempts': 50, 'failed_logins': 48, 'bytes_transferred': 5000000, 'packets': 50000, 'source_port': 1024, 'destination_port': 445}
pred, conf, threat, score = detector.predict(features)
print(f'Suspicious: {threat} - Risk Score = {score:.1f}')
"
```

## 📁 Project Structure

```
cyber-defense-framework/
├── app.py                    # Main Flask app
├── requirements.txt          # Dependencies
├── setup.py                  # Database setup
├── start.sh / start.bat      # Quick start scripts
├── backend/
│   ├── models/              # Database models
│   ├── routes/              # API endpoints
│   └── services/            # ML & business logic
├── ml/models/               # Trained ML models
├── templates/               # HTML pages
├── static/                  # CSS & JavaScript
├── data/                    # Training & sample data
└── README.md               # Full documentation
```

## 🔧 Troubleshooting

**Port 5000 already in use?**
```bash
# Linux/Mac: Kill process
lsof -ti:5000 | xargs kill -9

# Windows: Change port in app.py
app.run(debug=True, host='0.0.0.0', port=8000)
```

**Dependencies not installing?**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Database locked?**
```bash
rm database/cyber_defense.db
python setup.py
```

## ✅ Verification

```bash
# Check all components
python3 -c "
import flask
import pandas
import sklearn
import joblib
print('✓ All dependencies installed')
"
```

## 📱 API Testing

**Get Dashboard Stats:**
```bash
curl http://localhost:5000/api/dashboard
```

**Detect Threat:**
```bash
curl -X POST http://localhost:5000/api/detect \
  -H 'Content-Type: application/json' \
  -d '{"login_attempts": 50, "failed_logins": 48, "bytes_transferred": 5000000, "packets": 50000, "source_port": 1024, "destination_port": 445}'
```

## 🎓 Learning

- ML Models: `backend/services/threat_detector.py`
- API Routes: `backend/routes/`
- Frontend: `templates/` and `static/`
- Database: `backend/models/`

## 📚 Next Steps

1. **Explore Dashboard** - View threat analytics
2. **Upload Logs** - Test with sample CSV
3. **Train Model** - Improve detection accuracy
4. **Create Incidents** - Test workflow
5. **Review Responses** - Understand actions
6. **Read Code** - Learn implementation

---

**Need Help?** Check README.md for detailed documentation

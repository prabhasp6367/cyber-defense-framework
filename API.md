# API REFERENCE - AI Cyber Defense Framework

## Base URL
```
http://localhost:5000
```

## Authentication
All endpoints require login. Use session cookies.

```bash
POST /login
Body: {"username": "admin", "password": "password123"}
```

---

## 🔐 Authentication Endpoints

### Login
```
POST /login
Content-Type: application/json

{
  "username": "admin",
  "password": "password123"
}

Response: 200 OK
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@local",
    "role": "admin"
  }
}
```

### Logout
```
GET /logout

Response: 302 Redirect to /
```

### Get Profile
```
GET /api/user/profile

Response: 200 OK
{
  "id": 1,
  "username": "admin",
  "role": "admin",
  "is_active": true
}
```

---

## 📊 Dashboard Endpoints

### Dashboard Statistics
```
GET /api/dashboard

Response: 200 OK
{
  "total_events": 12485,
  "threats_detected": 327,
  "critical_alerts": 18,
  "incidents": 42,
  "blocked_events": 291,
  "system_health": 98.7,
  "events_24h": 1243,
  "threat_types": [
    {"type": "Brute Force", "count": 45},
    {"type": "Port Scanning", "count": 32}
  ],
  "severity_distribution": [
    {"severity": "critical", "count": 18},
    {"severity": "high", "count": 65}
  ]
}
```

### Threat Timeline (24h)
```
GET /api/dashboard/threats-timeline

Response: 200 OK
[
  {
    "time": "00:00",
    "total_events": 85,
    "suspicious_events": 12
  },
  {
    "time": "01:00",
    "total_events": 92,
    "suspicious_events": 15
  }
]
```

---

## 📝 Log Endpoints

### Get Logs
```
GET /api/logs?page=1&per_page=20&source_ip=192.168.1.50&severity=high

Response: 200 OK
{
  "total": 5432,
  "pages": 272,
  "current_page": 1,
  "logs": [
    {
      "id": 1,
      "timestamp": "2024-08-19T10:30:45",
      "source_ip": "192.168.1.50",
      "destination_ip": "10.0.0.1",
      "source_port": 54321,
      "destination_port": 443,
      "protocol": "TCP",
      "event_type": "Normal Login",
      "bytes_transferred": 50000,
      "packets": 120,
      "login_attempts": 1,
      "failed_logins": 0,
      "status": "success",
      "risk_score": 5.0,
      "severity": "low",
      "prediction": false,
      "confidence": 0.98
    }
  ]
}
```

### Upload CSV Logs
```
POST /api/logs/upload
Content-Type: multipart/form-data

Form Data:
  file: <CSV file>

Response: 201 Created
{
  "message": "File uploaded successfully",
  "imported_count": 1250,
  "filename": "logs.csv"
}
```

### Search Logs
```
GET /api/logs/search?q=192.168.1.50

Response: 200 OK
[
  {...log objects...}
]
```

### Get Log Detail
```
GET /api/logs/1

Response: 200 OK
{...log object...}
```

---

## 🧠 AI Detection Endpoints

### Detect Threat (Single)
```
POST /api/detect
Content-Type: application/json

{
  "login_attempts": 50,
  "failed_logins": 48,
  "bytes_transferred": 5000000,
  "packets": 50000,
  "source_port": 1024,
  "destination_port": 445,
  "source_ip": "203.0.113.50",
  "destination_ip": "10.0.0.1"
}

Response: 200 OK
{
  "prediction": "suspicious",
  "threat_type": "Brute Force",
  "risk_score": 87.5,
  "severity": "critical",
  "confidence": 0.96,
  "recommendation": "Block source IP, enforce account lockout policy, enable MFA",
  "alert_created": true,
  "alert_id": "ALERT-20240819105030"
}
```

### Batch Detection
```
POST /api/detect/batch
Content-Type: application/json

{
  "logs": [
    {"id": 1, "login_attempts": 1, "failed_logins": 0, ...},
    {"id": 2, "login_attempts": 50, "failed_logins": 48, ...}
  ]
}

Response: 200 OK
{
  "total": 2,
  "results": [
    {
      "log_id": 1,
      "prediction": "normal",
      "threat_type": null,
      "risk_score": 5.0,
      "severity": "low"
    },
    {
      "log_id": 2,
      "prediction": "suspicious",
      "threat_type": "Brute Force",
      "risk_score": 87.5,
      "severity": "critical"
    }
  ]
}
```

---

## 🚨 Alert Endpoints

### Get Alerts
```
GET /api/alerts?page=1&per_page=20&status=open&severity=critical

Response: 200 OK
{
  "total": 143,
  "pages": 8,
  "current_page": 1,
  "alerts": [
    {
      "id": 1,
      "alert_id": "ALERT-001",
      "timestamp": "2024-08-19T10:30:45",
      "threat_type": "Brute Force",
      "source_ip": "203.0.113.50",
      "destination_ip": "10.0.0.1",
      "severity": "critical",
      "risk_score": 87.5,
      "detection_method": "Random Forest",
      "status": "open",
      "recommended_action": "Block source IP, enable MFA",
      "created_at": "2024-08-19T10:30:45",
      "updated_at": "2024-08-19T10:30:45"
    }
  ]
}
```

### Alert Summary
```
GET /api/alerts/summary

Response: 200 OK
{
  "by_status": [
    {"status": "open", "count": 45},
    {"status": "investigating", "count": 12},
    {"status": "resolved", "count": 86}
  ],
  "by_severity": [
    {"severity": "critical", "count": 18},
    {"severity": "high", "count": 65},
    {"severity": "medium", "count": 45},
    {"severity": "low", "count": 15}
  ]
}
```

### Update Alert Status
```
PUT /api/alerts/1/status
Content-Type: application/json

{
  "status": "investigating"
}

Response: 200 OK
{...alert object...}
```

### Close Alert
```
POST /api/alerts/1/close

Response: 200 OK
{
  "message": "Alert resolved",
  "alert": {...}
}
```

---

## 🎯 Incident Endpoints

### Get Incidents
```
GET /api/incidents?page=1&per_page=20&status=open&severity=high

Response: 200 OK
{
  "total": 42,
  "pages": 3,
  "current_page": 1,
  "incidents": [
    {
      "id": 1,
      "incident_id": "INC-00001",
      "title": "Brute Force Attack on Admin Account",
      "threat_type": "Brute Force",
      "severity": "critical",
      "risk_score": 87.5,
      "status": "open",
      "assigned_analyst": "John Doe",
      "source_ip": "203.0.113.50",
      "created_at": "2024-08-19T10:30:45",
      "updated_at": "2024-08-19T10:30:45",
      "resolved_at": null
    }
  ]
}
```

### Create Incident
```
POST /api/incidents
Content-Type: application/json

{
  "title": "Suspicious Data Transfer",
  "description": "Large data transfer detected",
  "threat_type": "Data Exfiltration",
  "severity": "high",
  "risk_score": 75.5,
  "source_ip": "192.168.1.100"
}

Response: 201 Created
{...incident object...}
```

### Update Incident
```
PUT /api/incidents/1
Content-Type: application/json

{
  "status": "resolved",
  "assigned_analyst": "Jane Smith",
  "mitigation_steps": "Blocked IP, enabled MFA",
  "root_cause": "Compromised credentials"
}

Response: 200 OK
{...incident object...}
```

---

## ⚡ Response Endpoints

### Simulate Response
```
POST /api/response/simulate
Content-Type: application/json

{
  "incident_id": "INC-00001",
  "action": "Simulate IP Block",
  "action_type": "block_ip",
  "target": "203.0.113.50",
  "reason": "Brute force attack detected",
  "severity": "critical"
}

Response: 201 Created
{
  "message": "Simulated response executed successfully",
  "response": {
    "id": 1,
    "response_id": "RESP-00001",
    "incident_id": "INC-00001",
    "action": "Simulate IP Block",
    "action_type": "block_ip",
    "target": "203.0.113.50",
    "reason": "Brute force attack detected",
    "status": "completed",
    "simulation": true,
    "result": "SIMULATED: IP 203.0.113.50 would be added to firewall blocklist",
    "created_at": "2024-08-19T10:30:45",
    "executed_at": "2024-08-19T10:30:45"
  }
}
```

### Get Response History
```
GET /api/responses?page=1&per_page=20

Response: 200 OK
{
  "total": 87,
  "pages": 5,
  "current_page": 1,
  "responses": [...]
}
```

---

## 📈 Analytics Endpoints

### Analytics Overview
```
GET /api/analytics/overview

Response: 200 OK
{
  "events": {
    "total": 12485,
    "last_7_days": 1435,
    "last_30_days": 5432
  },
  "threats": {
    "total": 327,
    "last_7_days": 45,
    "detection_rate": 2.62
  },
  "alerts": {
    "total": 143,
    "critical": 18
  },
  "incidents": {
    "total": 42,
    "open": 12,
    "resolved": 28
  }
}
```

### Threat Trends
```
GET /api/analytics/threat-trends?days=30

Response: 200 OK
[
  {
    "date": "2024-08-19",
    "total_events": 415,
    "detected_threats": 32
  },
  {
    "date": "2024-08-18",
    "total_events": 402,
    "detected_threats": 28
  }
]
```

---

## 🔧 System Status

```
GET /api/system-status

Response: 200 OK
{
  "ml_engine": "online",
  "database": "online",
  "log_collector": "online",
  "detection_engine": "online",
  "response_engine": "simulation_mode",
  "api": "online",
  "timestamp": "2024-08-19T15:30:45"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid input parameters"
}
```

### 401 Unauthorized
```json
{
  "error": "Login required"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Rate Limiting

- No rate limiting in demo mode
- Production: Implement rate limiting per endpoint

## Authentication

- Session-based authentication
- Secure password hashing with Werkzeug
- CSRF protection enabled

---

**For more details, see README.md**

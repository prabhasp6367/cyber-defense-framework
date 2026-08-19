"""Threat detection routes using ML model"""
from flask import Blueprint, request, jsonify
from flask_login import login_required
from app import db
from backend.models import SecurityLog, Alert
from backend.services.threat_detector import ThreatDetector
from datetime import datetime

detection_bp = Blueprint('detection', __name__)

# Initialize threat detector
detector = ThreatDetector()

@detection_bp.route('/api/detect', methods=['POST'])
@login_required
def detect_threat():
    """Analyze security log and detect threats"""
    data = request.get_json()
    
    # Extract features from log data
    features = {
        'login_attempts': data.get('login_attempts', 0),
        'failed_logins': data.get('failed_logins', 0),
        'bytes_transferred': data.get('bytes_transferred', 0),
        'packets': data.get('packets', 0),
        'source_port': data.get('source_port', 0),
        'destination_port': data.get('destination_port', 0)
    }
    
    # Get prediction from ML model
    prediction, confidence, threat_type, risk_score = detector.predict(features)
    
    # Determine severity
    if risk_score >= 76:
        severity = 'critical'
    elif risk_score >= 51:
        severity = 'high'
    elif risk_score >= 26:
        severity = 'medium'
    else:
        severity = 'low'
    
    result = {
        'prediction': 'suspicious' if prediction == 1 else 'normal',
        'threat_type': threat_type,
        'risk_score': float(risk_score),
        'severity': severity,
        'confidence': float(confidence),
        'recommendation': get_recommendation(threat_type, severity)
    }
    
    # If threat detected and risk score is high, create alert
    if prediction == 1 and risk_score > 50:
        alert = Alert(
            alert_id=f"ALERT-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            timestamp=datetime.utcnow(),
            threat_type=threat_type,
            source_ip=data.get('source_ip', '0.0.0.0'),
            destination_ip=data.get('destination_ip', '0.0.0.0'),
            severity=severity,
            risk_score=risk_score,
            detection_method='Random Forest',
            status='open',
            description=f"Automated threat detection: {threat_type}",
            recommended_action=result['recommendation']
        )
        db.session.add(alert)
        db.session.commit()
        result['alert_created'] = True
        result['alert_id'] = alert.alert_id
    
    return jsonify(result)

@detection_bp.route('/api/detect/batch', methods=['POST'])
@login_required
def detect_batch():
    """Batch analyze multiple logs"""
    data = request.get_json()
    logs = data.get('logs', [])
    
    results = []
    for log in logs:
        features = {
            'login_attempts': log.get('login_attempts', 0),
            'failed_logins': log.get('failed_logins', 0),
            'bytes_transferred': log.get('bytes_transferred', 0),
            'packets': log.get('packets', 0),
            'source_port': log.get('source_port', 0),
            'destination_port': log.get('destination_port', 0)
        }
        
        prediction, confidence, threat_type, risk_score = detector.predict(features)
        
        if risk_score >= 76:
            severity = 'critical'
        elif risk_score >= 51:
            severity = 'high'
        elif risk_score >= 26:
            severity = 'medium'
        else:
            severity = 'low'
        
        results.append({
            'log_id': log.get('id'),
            'prediction': 'suspicious' if prediction == 1 else 'normal',
            'threat_type': threat_type,
            'risk_score': float(risk_score),
            'severity': severity,
            'confidence': float(confidence)
        })
    
    return jsonify({'total': len(results), 'results': results})

def get_recommendation(threat_type, severity):
    """Get security recommendation based on threat type"""
    recommendations = {
        'Brute Force': 'Block source IP, enforce account lockout policy, enable MFA',
        'Port Scanning': 'Implement network segmentation, enable IDS/IPS',
        'Suspicious Login': 'Review login activity, check for compromised credentials',
        'Malware Indicator': 'Isolate affected system, run antivirus scan',
        'Data Exfiltration Pattern': 'Block outbound connections, investigate data access',
        'Abnormal Network Traffic': 'Inspect packet payloads, review firewall logs',
        'Privilege Escalation Indicator': 'Review sudo/admin logs, audit system permissions',
        'Denial-of-Service Pattern': 'Enable rate limiting, engage DDoS mitigation',
        'Credential Attack Pattern': 'Force password reset, enable MFA',
        'Anomalous Activity': 'Investigate unusual behavior patterns'
    }
    
    return recommendations.get(threat_type, 'Investigate incident and take appropriate action')

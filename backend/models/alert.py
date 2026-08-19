"""Alert model for threat detections"""
from app import db
from datetime import datetime

class Alert(db.Model):
    """Security alert for detected threats"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.String(20), unique=True, nullable=False)  # ALERT-001, etc.
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    threat_type = db.Column(db.String(50), nullable=False)  # Brute Force, Port Scan, etc.
    source_ip = db.Column(db.String(45), nullable=False)
    destination_ip = db.Column(db.String(45))
    severity = db.Column(db.String(20), nullable=False)  # low, medium, high, critical
    risk_score = db.Column(db.Float, nullable=False)
    detection_method = db.Column(db.String(50))  # Random Forest, Isolation Forest, Rule-based
    status = db.Column(db.String(20), default='open')  # open, investigating, resolved
    recommended_action = db.Column(db.Text)
    description = db.Column(db.Text)
    related_logs = db.Column(db.String(500))  # JSON string of log IDs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'alert_id': self.alert_id,
            'timestamp': self.timestamp.isoformat(),
            'threat_type': self.threat_type,
            'source_ip': self.source_ip,
            'destination_ip': self.destination_ip,
            'severity': self.severity,
            'risk_score': self.risk_score,
            'detection_method': self.detection_method,
            'status': self.status,
            'recommended_action': self.recommended_action,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

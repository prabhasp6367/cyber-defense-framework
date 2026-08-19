"""Security Log model"""
from app import db
from datetime import datetime

class SecurityLog(db.Model):
    """Security log entry"""
    __tablename__ = 'security_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    source_ip = db.Column(db.String(45), nullable=False)  # IPv4 or IPv6
    destination_ip = db.Column(db.String(45), nullable=False)
    source_port = db.Column(db.Integer)
    destination_port = db.Column(db.Integer)
    protocol = db.Column(db.String(20))  # TCP, UDP, ICMP, etc.
    event_type = db.Column(db.String(50), nullable=False)
    bytes_transferred = db.Column(db.Integer, default=0)
    packets = db.Column(db.Integer, default=0)
    login_attempts = db.Column(db.Integer, default=0)
    failed_logins = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20))  # success, failed, pending
    risk_score = db.Column(db.Float, default=0.0)
    severity = db.Column(db.String(20), default='low')  # low, medium, high, critical
    prediction = db.Column(db.Boolean, default=False)  # True = suspicious, False = normal
    confidence = db.Column(db.Float, default=0.0)
    raw_data = db.Column(db.Text)  # Store original log line
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'source_ip': self.source_ip,
            'destination_ip': self.destination_ip,
            'source_port': self.source_port,
            'destination_port': self.destination_port,
            'protocol': self.protocol,
            'event_type': self.event_type,
            'bytes_transferred': self.bytes_transferred,
            'packets': self.packets,
            'login_attempts': self.login_attempts,
            'failed_logins': self.failed_logins,
            'status': self.status,
            'risk_score': self.risk_score,
            'severity': self.severity,
            'prediction': self.prediction,
            'confidence': self.confidence
        }

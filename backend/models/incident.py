"""Incident model for tracking security incidents"""
from app import db
from datetime import datetime

class Incident(db.Model):
    """Security incident tracking"""
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.String(20), unique=True, nullable=False)  # INC-001, etc.
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    threat_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # low, medium, high, critical
    risk_score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='open')  # open, investigating, contained, resolved
    assigned_analyst = db.Column(db.String(80))
    source_ip = db.Column(db.String(45))
    affected_systems = db.Column(db.Text)  # JSON array
    related_alerts = db.Column(db.Text)  # JSON array of alert IDs
    mitigation_steps = db.Column(db.Text)
    root_cause = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'incident_id': self.incident_id,
            'title': self.title,
            'description': self.description,
            'threat_type': self.threat_type,
            'severity': self.severity,
            'risk_score': self.risk_score,
            'status': self.status,
            'assigned_analyst': self.assigned_analyst,
            'source_ip': self.source_ip,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }

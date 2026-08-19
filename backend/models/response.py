"""Response model for security response actions"""
from app import db
from datetime import datetime

class Response(db.Model):
    """Simulated security response action"""
    __tablename__ = 'responses'
    
    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.String(20), unique=True, nullable=False)  # RESP-001, etc.
    incident_id = db.Column(db.String(20), db.ForeignKey('incidents.incident_id'))
    action = db.Column(db.String(100), nullable=False)  # IP Block, Account Lock, Session Termination, etc.
    action_type = db.Column(db.String(50))  # block_ip, lock_account, terminate_session, escalate, etc.
    target = db.Column(db.String(100))  # IP, username, session_id, etc.
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, executing, completed, failed
    simulation = db.Column(db.Boolean, default=True)  # Always True for safety
    result = db.Column(db.Text)
    severity_level = db.Column(db.String(20))  # low, medium, high, critical
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    executed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'response_id': self.response_id,
            'incident_id': self.incident_id,
            'action': self.action,
            'action_type': self.action_type,
            'target': self.target,
            'reason': self.reason,
            'status': self.status,
            'simulation': self.simulation,
            'result': self.result,
            'created_at': self.created_at.isoformat(),
            'executed_at': self.executed_at.isoformat() if self.executed_at else None
        }

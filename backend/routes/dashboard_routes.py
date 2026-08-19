"""Dashboard routes"""
from flask import Blueprint, jsonify, render_template
from flask_login import login_required
from app import db
from backend.models import SecurityLog, Alert, Incident
from datetime import datetime, timedelta
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@dashboard_bp.route('/api/dashboard')
@login_required
def get_dashboard_stats():
    """Get dashboard statistics"""
    
    # Get counts
    total_events = SecurityLog.query.count()
    threats_detected = SecurityLog.query.filter_by(prediction=True).count()
    critical_alerts = Alert.query.filter_by(severity='critical').count()
    incidents = Incident.query.filter_by(status='open').count()
    blocked_events = SecurityLog.query.filter_by(status='blocked').count()
    
    # Calculate system health (simplified)
    system_health = 98.7
    
    # Get events from last 24 hours
    last_24h = datetime.utcnow() - timedelta(hours=24)
    events_24h = SecurityLog.query.filter(SecurityLog.timestamp >= last_24h).count()
    
    # Get threat breakdown by type
    threat_types = db.session.query(
        SecurityLog.event_type,
        func.count(SecurityLog.id).label('count')
    ).filter(SecurityLog.prediction == True).group_by(SecurityLog.event_type).all()
    
    # Get severity distribution
    severity_dist = db.session.query(
        Alert.severity,
        func.count(Alert.id).label('count')
    ).group_by(Alert.severity).all()
    
    return jsonify({
        'total_events': total_events,
        'threats_detected': threats_detected,
        'critical_alerts': critical_alerts,
        'incidents': incidents,
        'blocked_events': blocked_events,
        'system_health': system_health,
        'events_24h': events_24h,
        'threat_types': [{'type': t[0], 'count': t[1]} for t in threat_types],
        'severity_distribution': [{'severity': s[0], 'count': s[1]} for s in severity_dist]
    })

@dashboard_bp.route('/api/dashboard/threats-timeline')
@login_required
def threats_timeline():
    """Get threat timeline data for charts"""
    # Get hourly threat data for last 24 hours
    last_24h = datetime.utcnow() - timedelta(hours=24)
    
    hourly_data = db.session.query(
        func.strftime('%H:00', SecurityLog.timestamp).label('hour'),
        func.count(SecurityLog.id).label('total'),
        func.sum(func.cast(SecurityLog.prediction, db.Integer)).label('suspicious')
    ).filter(SecurityLog.timestamp >= last_24h).group_by(
        func.strftime('%H:00', SecurityLog.timestamp)
    ).all()
    
    data = []
    for hour, total, suspicious in hourly_data:
        data.append({
            'time': hour,
            'total_events': total,
            'suspicious_events': suspicious or 0
        })
    
    return jsonify(data)

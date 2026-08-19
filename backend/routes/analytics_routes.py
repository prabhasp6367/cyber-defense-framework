"""Analytics routes"""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app import db
from backend.models import SecurityLog, Alert, Incident, ModelMetric
from sqlalchemy import func
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
@login_required
def analytics_page():
    """Analytics page"""
    return render_template('analytics.html')

@analytics_bp.route('/api/analytics/overview', methods=['GET'])
@login_required
def analytics_overview():
    """Get analytics overview"""
    last_7d = datetime.utcnow() - timedelta(days=7)
    last_30d = datetime.utcnow() - timedelta(days=30)
    
    # Event statistics
    total_events = SecurityLog.query.count()
    events_7d = SecurityLog.query.filter(SecurityLog.timestamp >= last_7d).count()
    events_30d = SecurityLog.query.filter(SecurityLog.timestamp >= last_30d).count()
    
    # Threat statistics
    total_threats = SecurityLog.query.filter_by(prediction=True).count()
    threats_7d = SecurityLog.query.filter(
        (SecurityLog.prediction == True) & (SecurityLog.timestamp >= last_7d)
    ).count()
    
    # Alert statistics
    total_alerts = Alert.query.count()
    critical_alerts = Alert.query.filter_by(severity='critical').count()
    
    # Incident statistics
    total_incidents = Incident.query.count()
    open_incidents = Incident.query.filter_by(status='open').count()
    resolved_incidents = Incident.query.filter_by(status='resolved').count()
    
    return jsonify({
        'events': {
            'total': total_events,
            'last_7_days': events_7d,
            'last_30_days': events_30d
        },
        'threats': {
            'total': total_threats,
            'last_7_days': threats_7d,
            'detection_rate': (total_threats / total_events * 100) if total_events > 0 else 0
        },
        'alerts': {
            'total': total_alerts,
            'critical': critical_alerts
        },
        'incidents': {
            'total': total_incidents,
            'open': open_incidents,
            'resolved': resolved_incidents
        }
    })

@analytics_bp.route('/api/analytics/threat-trends', methods=['GET'])
@login_required
def threat_trends():
    """Get threat trends over time"""
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    daily_threats = db.session.query(
        func.date(SecurityLog.timestamp).label('date'),
        func.count(SecurityLog.id).label('total'),
        func.sum(func.cast(SecurityLog.prediction, db.Integer)).label('threats')
    ).filter(SecurityLog.timestamp >= start_date).group_by(
        func.date(SecurityLog.timestamp)
    ).all()
    
    return jsonify([{
        'date': str(date),
        'total_events': total,
        'detected_threats': threats or 0
    } for date, total, threats in daily_threats])

@analytics_bp.route('/api/analytics/model-performance', methods=['GET'])
@login_required
def model_performance():
    """Get ML model performance metrics"""
    latest_model = ModelMetric.query.order_by(ModelMetric.trained_at.desc()).first()
    
    if not latest_model:
        return jsonify({
            'message': 'No model metrics available',
            'metrics': None
        })
    
    return jsonify(latest_model.to_dict())

@analytics_bp.route('/api/analytics/top-threats', methods=['GET'])
@login_required
def top_threats():
    """Get top detected threat types"""
    top = db.session.query(
        Alert.threat_type,
        func.count(Alert.id).label('count')
    ).group_by(Alert.threat_type).order_by(
        func.count(Alert.id).desc()
    ).limit(10).all()
    
    return jsonify([{
        'threat_type': t[0],
        'count': t[1]
    } for t in top])

@analytics_bp.route('/api/analytics/severity-distribution', methods=['GET'])
@login_required
def severity_distribution():
    """Get alert severity distribution"""
    dist = db.session.query(
        Alert.severity,
        func.count(Alert.id).label('count')
    ).group_by(Alert.severity).all()
    
    return jsonify([{
        'severity': s[0],
        'count': s[1]
    } for s in dist])

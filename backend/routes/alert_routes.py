"""Alert management routes"""
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app import db
from backend.models import Alert
from datetime import datetime

alert_bp = Blueprint('alerts', __name__)

@alert_bp.route('/alerts')
@login_required
def alerts_page():
    """Alerts page"""
    return render_template('alerts.html')

@alert_bp.route('/api/alerts', methods=['GET'])
@login_required
def get_alerts():
    """Get alerts with filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', '')
    severity = request.args.get('severity', '')
    
    query = Alert.query
    
    if status:
        query = query.filter_by(status=status)
    if severity:
        query = query.filter_by(severity=severity)
    
    alerts = query.order_by(Alert.timestamp.desc()).paginate(page, per_page)
    
    return jsonify({
        'total': alerts.total,
        'pages': alerts.pages,
        'current_page': page,
        'alerts': [alert.to_dict() for alert in alerts.items]
    })

@alert_bp.route('/api/alerts/summary', methods=['GET'])
@login_required
def alerts_summary():
    """Get summary of alerts by status and severity"""
    from sqlalchemy import func
    
    by_status = db.session.query(
        Alert.status,
        func.count(Alert.id).label('count')
    ).group_by(Alert.status).all()
    
    by_severity = db.session.query(
        Alert.severity,
        func.count(Alert.id).label('count')
    ).group_by(Alert.severity).all()
    
    return jsonify({
        'by_status': [{'status': s[0], 'count': s[1]} for s in by_status],
        'by_severity': [{'severity': s[0], 'count': s[1]} for s in by_severity]
    })

@alert_bp.route('/api/alerts/<int:alert_id>', methods=['GET'])
@login_required
def get_alert(alert_id):
    """Get alert detail"""
    alert = Alert.query.get_or_404(alert_id)
    return jsonify(alert.to_dict())

@alert_bp.route('/api/alerts/<int:alert_id>/status', methods=['PUT'])
@login_required
def update_alert_status(alert_id):
    """Update alert status"""
    alert = Alert.query.get_or_404(alert_id)
    data = request.get_json()
    new_status = data.get('status')
    
    valid_statuses = ['open', 'investigating', 'resolved']
    if new_status not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400
    
    alert.status = new_status
    alert.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(alert.to_dict())

@alert_bp.route('/api/alerts/<int:alert_id>/close', methods=['POST'])
@login_required
def close_alert(alert_id):
    """Close/resolve alert"""
    alert = Alert.query.get_or_404(alert_id)
    alert.status = 'resolved'
    alert.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Alert resolved', 'alert': alert.to_dict()})

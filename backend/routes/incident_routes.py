"""Incident management routes"""
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app import db
from backend.models import Incident
from datetime import datetime

incident_bp = Blueprint('incidents', __name__)

@incident_bp.route('/incidents')
@login_required
def incidents_page():
    """Incidents page"""
    return render_template('incidents.html')

@incident_bp.route('/api/incidents', methods=['GET'])
@login_required
def get_incidents():
    """Get incidents with filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', '')
    severity = request.args.get('severity', '')
    
    query = Incident.query
    
    if status:
        query = query.filter_by(status=status)
    if severity:
        query = query.filter_by(severity=severity)
    
    incidents = query.order_by(Incident.created_at.desc()).paginate(page, per_page)
    
    return jsonify({
        'total': incidents.total,
        'pages': incidents.pages,
        'current_page': page,
        'incidents': [incident.to_dict() for incident in incidents.items]
    })

@incident_bp.route('/api/incidents', methods=['POST'])
@login_required
def create_incident():
    """Create new incident"""
    data = request.get_json()
    
    # Generate incident ID
    last_incident = db.session.query(Incident).order_by(Incident.id.desc()).first()
    incident_num = (last_incident.id + 1) if last_incident else 1
    incident_id = f"INC-{incident_num:05d}"
    
    incident = Incident(
        incident_id=incident_id,
        title=data.get('title'),
        description=data.get('description'),
        threat_type=data.get('threat_type'),
        severity=data.get('severity', 'medium'),
        risk_score=float(data.get('risk_score', 0)),
        source_ip=data.get('source_ip'),
        assigned_analyst=data.get('assigned_analyst', 'Unassigned')
    )
    
    db.session.add(incident)
    db.session.commit()
    
    return jsonify(incident.to_dict()), 201

@incident_bp.route('/api/incidents/<int:incident_id>', methods=['GET'])
@login_required
def get_incident(incident_id):
    """Get incident detail"""
    incident = Incident.query.get_or_404(incident_id)
    return jsonify(incident.to_dict())

@incident_bp.route('/api/incidents/<int:incident_id>', methods=['PUT'])
@login_required
def update_incident(incident_id):
    """Update incident"""
    incident = Incident.query.get_or_404(incident_id)
    data = request.get_json()
    
    if 'status' in data:
        incident.status = data['status']
    if 'assigned_analyst' in data:
        incident.assigned_analyst = data['assigned_analyst']
    if 'mitigation_steps' in data:
        incident.mitigation_steps = data['mitigation_steps']
    if 'root_cause' in data:
        incident.root_cause = data['root_cause']
    
    incident.updated_at = datetime.utcnow()
    
    if data.get('status') == 'resolved':
        incident.resolved_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify(incident.to_dict())

@incident_bp.route('/api/incidents/summary', methods=['GET'])
@login_required
def incidents_summary():
    """Get incident summary statistics"""
    from sqlalchemy import func
    
    by_status = db.session.query(
        Incident.status,
        func.count(Incident.id).label('count')
    ).group_by(Incident.status).all()
    
    by_severity = db.session.query(
        Incident.severity,
        func.count(Incident.id).label('count')
    ).group_by(Incident.severity).all()
    
    return jsonify({
        'by_status': [{'status': s[0], 'count': s[1]} for s in by_status],
        'by_severity': [{'severity': s[0], 'count': s[1]} for s in by_severity]
    })

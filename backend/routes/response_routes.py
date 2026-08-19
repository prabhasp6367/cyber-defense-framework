"""Security response simulation routes"""
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app import db
from backend.models import Response, Incident
from datetime import datetime

response_bp = Blueprint('response', __name__)

@response_bp.route('/response')
@login_required
def response_center():
    """Response center page"""
    return render_template('response.html')

@response_bp.route('/api/response/simulate', methods=['POST'])
@login_required
def simulate_response():
    """Simulate security response action"""
    data = request.get_json()
    
    incident_id = data.get('incident_id')
    action = data.get('action')
    action_type = data.get('action_type')
    target = data.get('target')
    reason = data.get('reason')
    severity = data.get('severity', 'medium')
    
    # Generate response ID
    last_response = db.session.query(Response).order_by(Response.id.desc()).first()
    response_num = (last_response.id + 1) if last_response else 1
    response_id = f"RESP-{response_num:05d}"
    
    # Simulate response execution
    result = simulate_action(action_type, target)
    
    response = Response(
        response_id=response_id,
        incident_id=incident_id,
        action=action,
        action_type=action_type,
        target=target,
        reason=reason,
        status='completed',
        simulation=True,
        result=result,
        severity_level=severity,
        executed_at=datetime.utcnow()
    )
    
    db.session.add(response)
    db.session.commit()
    
    return jsonify({
        'message': 'Simulated response executed successfully',
        'response': response.to_dict()
    }), 201

@response_bp.route('/api/responses', methods=['GET'])
@login_required
def get_responses():
    """Get all simulated responses"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    responses = Response.query.order_by(Response.created_at.desc()).paginate(page, per_page)
    
    return jsonify({
        'total': responses.total,
        'pages': responses.pages,
        'current_page': page,
        'responses': [r.to_dict() for r in responses.items]
    })

def simulate_action(action_type, target):
    """Simulate security action execution"""
    simulations = {
        'block_ip': f"SIMULATED: IP {target} would be added to firewall blocklist",
        'lock_account': f"SIMULATED: Account {target} would be locked for 30 minutes",
        'terminate_session': f"SIMULATED: Session {target} would be terminated immediately",
        'escalate': f"SIMULATED: Alert escalated to senior SOC analyst",
        'isolate_system': f"SIMULATED: System {target} would be isolated from network",
        'revoke_token': f"SIMULATED: Token {target} would be revoked",
        'enable_mfa': f"SIMULATED: MFA would be enforced for {target}",
        'reset_password': f"SIMULATED: Password reset required for {target}",
        'collect_evidence': f"SIMULATED: Forensic evidence collected from {target}",
        'notify_admin': f"SIMULATED: System administrator notified about {target}"
    }
    
    return simulations.get(action_type, f"SIMULATED: Action on {target} would be executed")

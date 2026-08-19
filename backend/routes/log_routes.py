"""Security log routes"""
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app import db
from backend.models import SecurityLog
from werkzeug.utils import secure_filename
import csv
import os
from datetime import datetime

log_bp = Blueprint('logs', __name__)

ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = 'uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@log_bp.route('/logs')
@login_required
def logs_page():
    """Security logs page"""
    return render_template('logs.html')

@log_bp.route('/api/logs', methods=['GET'])
@login_required
def get_logs():
    """Get security logs with pagination and filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Filter parameters
    source_ip = request.args.get('source_ip', '')
    event_type = request.args.get('event_type', '')
    severity = request.args.get('severity', '')
    
    query = SecurityLog.query
    
    if source_ip:
        query = query.filter_by(source_ip=source_ip)
    if event_type:
        query = query.filter_by(event_type=event_type)
    if severity:
        query = query.filter_by(severity=severity)
    
    logs = query.order_by(SecurityLog.timestamp.desc()).paginate(page, per_page)
    
    return jsonify({
        'total': logs.total,
        'pages': logs.pages,
        'current_page': page,
        'logs': [log.to_dict() for log in logs.items]
    })

@log_bp.route('/api/logs/upload', methods=['POST'])
@login_required
def upload_logs():
    """Upload and parse CSV log file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only CSV files allowed'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Parse CSV and insert into database
        imported_count = 0
        with open(filepath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    log_entry = SecurityLog(
                        timestamp=datetime.fromisoformat(row.get('timestamp', datetime.utcnow().isoformat())),
                        source_ip=row.get('source_ip', '0.0.0.0'),
                        destination_ip=row.get('destination_ip', '0.0.0.0'),
                        source_port=int(row.get('source_port', 0)) if row.get('source_port') else None,
                        destination_port=int(row.get('destination_port', 0)) if row.get('destination_port') else None,
                        protocol=row.get('protocol', 'TCP'),
                        event_type=row.get('event_type', 'Unknown'),
                        bytes_transferred=int(row.get('bytes_transferred', 0)) if row.get('bytes_transferred') else 0,
                        packets=int(row.get('packets', 0)) if row.get('packets') else 0,
                        login_attempts=int(row.get('login_attempts', 0)) if row.get('login_attempts') else 0,
                        failed_logins=int(row.get('failed_logins', 0)) if row.get('failed_logins') else 0,
                        status=row.get('status', 'pending'),
                        raw_data=str(row)
                    )
                    db.session.add(log_entry)
                    imported_count += 1
                except Exception as e:
                    print(f"Error processing row: {e}")
                    continue
        
        db.session.commit()
        return jsonify({
            'message': 'File uploaded successfully',
            'imported_count': imported_count,
            'filename': filename
        }), 201
    
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@log_bp.route('/api/logs/search', methods=['GET'])
@login_required
def search_logs():
    """Search logs by IP or event type"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    results = SecurityLog.query.filter(
        (SecurityLog.source_ip.ilike(f'%{query}%')) |
        (SecurityLog.destination_ip.ilike(f'%{query}%')) |
        (SecurityLog.event_type.ilike(f'%{query}%'))
    ).limit(50).all()
    
    return jsonify([log.to_dict() for log in results])

@log_bp.route('/api/logs/<int:log_id>', methods=['GET'])
@login_required
def get_log_detail(log_id):
    """Get detailed log information"""
    log = SecurityLog.query.get_or_404(log_id)
    return jsonify(log.to_dict())

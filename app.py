"""Main Flask Application for AI-Driven Cyber Defense Framework"""
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/cyber_defense.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create uploads directory if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

if not os.path.exists('database'):
    os.makedirs('database')

# Import routes and models
from backend.routes import auth_routes, dashboard_routes, log_routes, detection_routes, alert_routes, incident_routes, response_routes, analytics_routes
from backend.models import User

# Register blueprints
app.register_blueprint(auth_routes.auth_bp)
app.register_blueprint(dashboard_routes.dashboard_bp)
app.register_blueprint(log_routes.log_bp)
app.register_blueprint(detection_routes.detection_bp)
app.register_blueprint(alert_routes.alert_bp)
app.register_blueprint(incident_routes.incident_bp)
app.register_blueprint(response_routes.response_bp)
app.register_blueprint(analytics_routes.analytics_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/api/system-status')
def system_status():
    """Get system status"""
    return jsonify({
        'ml_engine': 'online',
        'database': 'online',
        'log_collector': 'online',
        'detection_engine': 'online',
        'response_engine': 'simulation_mode',
        'api': 'online',
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

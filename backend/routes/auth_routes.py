"""Authentication routes"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from backend.models import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            if request.is_json:
                return jsonify({'error': 'Username and password required'}), 400
            return render_template('login.html', error='Username and password required')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            if request.is_json:
                return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200
            return redirect(url_for('dashboard.dashboard'))
        else:
            if request.is_json:
                return jsonify({'error': 'Invalid credentials'}), 401
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user (demo only)"""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return jsonify({'error': 'All fields required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Registration successful', 'user': user.to_dict()}), 201

@auth_bp.route('/api/user/profile')
@login_required
def get_profile():
    """Get current user profile"""
    return jsonify(current_user.to_dict())

"""AI-based Threat Detection Engine using Random Forest"""
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
from datetime import datetime

class ThreatDetector:
    """AI-powered threat detection using Machine Learning"""
    
    def __init__(self, model_path='ml/models/threat_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_names = [
            'login_attempts', 'failed_logins', 'bytes_transferred',
            'packets', 'source_port', 'destination_port'
        ]
        self.load_model()
    
    def load_model(self):
        """Load pre-trained ML model"""
        if os.path.exists(self.model_path):
            try:
                model_data = joblib.load(self.model_path)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                print(f"Loaded model from {self.model_path}")
            except Exception as e:
                print(f"Error loading model: {e}. Using default model.")
                self.train_default_model()
        else:
            print("Model not found. Training default model...")
            self.train_default_model()
    
    def train_default_model(self):
        """Train a default Random Forest model with synthetic data"""
        # Create synthetic training data
        np.random.seed(42)
        n_samples = 1000
        
        # Normal activity samples
        normal_samples = np.random.randint(0, 10, (n_samples // 2, 6))
        normal_labels = np.zeros(n_samples // 2)
        
        # Suspicious activity samples
        suspicious_samples = np.random.randint(15, 100, (n_samples // 2, 6))
        suspicious_labels = np.ones(n_samples // 2)
        
        # Combine data
        X = np.vstack([normal_samples, suspicious_samples])
        y = np.hstack([normal_labels, suspicious_labels])
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Random Forest model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_scaled, y)
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler
        }, self.model_path)
        
        print(f"Model trained and saved to {self.model_path}")
    
    def predict(self, features_dict):
        """Predict threat and calculate risk score
        
        Args:
            features_dict: Dictionary with feature values
            
        Returns:
            tuple: (prediction, confidence, threat_type, risk_score)
        """
        # Extract features in correct order
        features = np.array([[
            features_dict.get('login_attempts', 0),
            features_dict.get('failed_logins', 0),
            features_dict.get('bytes_transferred', 0),
            features_dict.get('packets', 0),
            features_dict.get('source_port', 0),
            features_dict.get('destination_port', 0)
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Get prediction and probabilities
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        confidence = float(np.max(probabilities))
        
        # Calculate risk score (0-100)
        risk_score = self._calculate_risk_score(
            features[0],
            prediction,
            confidence
        )
        
        # Determine threat type
        threat_type = self._classify_threat_type(features[0])
        
        return int(prediction), confidence, threat_type, risk_score
    
    def _calculate_risk_score(self, features, prediction, confidence):
        """Calculate risk score based on features and prediction
        
        Risk Score Factors:
        - Failed login attempts (0-30 points)
        - Bytes transferred (0-25 points)
        - Unusual ports (0-20 points)
        - Packet count (0-15 points)
        - ML confidence (multiplier)
        """
        score = 0
        
        login_attempts, failed_logins, bytes_transferred, packets, source_port, dest_port = features
        
        # Factor 1: Failed login attempts (up to 30 points)
        if failed_logins > 0:
            score += min(30, failed_logins * 2.5)
        
        # Factor 2: Bytes transferred (up to 25 points)
        if bytes_transferred > 1000000:  # Over 1MB
            score += min(25, (bytes_transferred / 1000000) * 5)
        
        # Factor 3: Unusual ports (high port numbers, up to 20 points)
        if dest_port > 10000 or (dest_port < 1024 and dest_port not in [22, 80, 443]):
            score += 20
        
        # Factor 4: High packet count (up to 15 points)
        if packets > 1000:
            score += min(15, (packets / 1000) * 3)
        
        # Factor 5: ML model confidence boost (multiply base score)
        if prediction == 1:  # Suspicious
            score = min(100, score + (confidence * 30))
        else:
            score = max(0, score - (confidence * 15))
        
        return min(100, max(0, score))
    
    def _classify_threat_type(self, features):
        """Classify threat type based on feature patterns
        
        Args:
            features: Feature array
            
        Returns:
            str: Threat type classification
        """
        login_attempts, failed_logins, bytes_transferred, packets, source_port, dest_port = features
        
        # Rule-based threat classification
        if failed_logins >= 5:
            return 'Brute Force'
        
        if dest_port in [21, 22, 23, 25, 53, 110, 143, 445, 3306]:
            if packets > 100:
                return 'Port Scanning'
        
        if login_attempts > 0 and failed_logins > 0:
            if failed_logins / login_attempts > 0.7:
                return 'Credential Attack Pattern'
        
        if bytes_transferred > 5000000:  # Over 5MB
            return 'Data Exfiltration Pattern'
        
        if packets > 5000:
            return 'Abnormal Network Traffic'
        
        if dest_port == 445 or source_port == 445:  # SMB
            return 'Privilege Escalation Indicator'
        
        if packets > 50000:
            return 'Denial-of-Service Pattern'
        
        if source_port < 1024 and dest_port > 1024:
            return 'Suspicious Login'
        
        return 'Anomalous Activity'


class AnomalyDetector:
    """Unsupervised anomaly detection using Isolation Forest"""
    
    def __init__(self, model_path='ml/models/anomaly_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """Load or create anomaly detection model"""
        if os.path.exists(self.model_path):
            try:
                model_data = joblib.load(self.model_path)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                print(f"Loaded anomaly model from {self.model_path}")
            except Exception as e:
                print(f"Error loading anomaly model: {e}")
                self.train_model()
        else:
            self.train_model()
    
    def train_model(self):
        """Train Isolation Forest model"""
        # Create synthetic training data
        np.random.seed(42)
        X = np.random.randn(500, 6) * 10 + 50
        
        # Scale data
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Isolation Forest
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_scaled)
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler
        }, self.model_path)
        
        print(f"Anomaly model trained and saved to {self.model_path}")
    
    def detect_anomaly(self, features):
        """Detect anomalies in features
        
        Args:
            features: Feature array
            
        Returns:
            tuple: (is_anomaly, anomaly_score)
        """
        features_scaled = self.scaler.transform([features])
        prediction = self.model.predict(features_scaled)[0]
        
        # Get anomaly score (-1 to 1, where -1 is definitely anomalous)
        anomaly_score = self.model.score_samples(features_scaled)[0]
        
        # Convert to 0-100 scale
        anomaly_score_normalized = ((anomaly_score + 1) / 2) * 100
        
        return prediction == -1, anomaly_score_normalized

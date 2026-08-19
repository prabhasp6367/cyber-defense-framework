"""ML Model Training Pipeline"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
import os
from datetime import datetime

class ModelTrainer:
    """Train ML models for threat detection"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.metrics = {}
        self.feature_names = [
            'login_attempts', 'failed_logins', 'bytes_transferred',
            'packets', 'source_port', 'destination_port'
        ]
    
    def load_data(self, filepath):
        """Load training data from CSV"""
        df = pd.read_csv(filepath)
        return df
    
    def preprocess_data(self, df):
        """Preprocess and clean data"""
        # Handle missing values
        df = df.fillna(0)
        
        # Extract features and labels
        X = df[self.feature_names].values
        y = df['label'].values
        
        return X, y
    
    def train(self, X, y, test_size=0.2):
        """Train Random Forest model
        
        Args:
            X: Features
            y: Labels (0=normal, 1=suspicious)
            test_size: Test set proportion
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        print("Training Random Forest model...")
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        # Calculate metrics
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'training_samples': len(X_train),
            'testing_samples': len(X_test),
            'model_version': datetime.now().strftime('%Y%m%d_%H%M%S')
        }
        
        print("\n=== Model Performance ===")
        print(f"Accuracy:  {self.metrics['accuracy']:.4f}")
        print(f"Precision: {self.metrics['precision']:.4f}")
        print(f"Recall:    {self.metrics['recall']:.4f}")
        print(f"F1-Score:  {self.metrics['f1_score']:.4f}")
        print(f"\nConfusion Matrix:\n{np.array(self.metrics['confusion_matrix'])}")
        
        return self.metrics
    
    def save_model(self, filepath):
        """Save trained model"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'metrics': self.metrics
        }, filepath)
        print(f"Model saved to {filepath}")
    
    def feature_importance(self):
        """Get feature importance from trained model"""
        if self.model is None:
            return None
        
        importance = self.model.feature_importances_
        feature_importance_dict = dict(zip(self.feature_names, importance))
        
        # Sort by importance
        sorted_features = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)
        
        print("\n=== Feature Importance ===")
        for feature, importance_val in sorted_features:
            print(f"{feature}: {importance_val:.4f}")
        
        return dict(sorted_features)

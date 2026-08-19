"""Model metrics for ML model performance tracking"""
from app import db
from datetime import datetime

class ModelMetric(db.Model):
    """ML model performance metrics"""
    __tablename__ = 'model_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    model_version = db.Column(db.String(50), unique=True, nullable=False)
    accuracy = db.Column(db.Float)
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    f1_score = db.Column(db.Float)
    true_positives = db.Column(db.Integer, default=0)
    true_negatives = db.Column(db.Integer, default=0)
    false_positives = db.Column(db.Integer, default=0)
    false_negatives = db.Column(db.Integer, default=0)
    training_samples = db.Column(db.Integer, default=0)
    testing_samples = db.Column(db.Integer, default=0)
    training_time = db.Column(db.Float)  # seconds
    model_path = db.Column(db.String(255))
    trained_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'model_version': self.model_version,
            'accuracy': self.accuracy,
            'precision': self.precision,
            'recall': self.recall,
            'f1_score': self.f1_score,
            'true_positives': self.true_positives,
            'true_negatives': self.true_negatives,
            'false_positives': self.false_positives,
            'false_negatives': self.false_negatives,
            'training_samples': self.training_samples,
            'testing_samples': self.testing_samples,
            'training_time': self.training_time,
            'trained_at': self.trained_at.isoformat()
        }

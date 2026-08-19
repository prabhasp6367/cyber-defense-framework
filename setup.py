"""Setup script - Initialize database and demo data"""
import os
from app import app, db
from backend.models import User
from backend.services.dataset_generator import DatasetGenerator
from backend.services.model_trainer import ModelTrainer
import sys

def setup():
    """Initialize database and create demo user"""
    print("\n" + "="*60)
    print("AI Cyber Defense Framework - Setup")
    print("="*60 + "\n")
    
    with app.app_context():
        # Create database tables
        print("[1/4] Creating database tables...")
        db.create_all()
        print("      ✓ Database tables created")
        
        # Create demo user
        print("\n[2/4] Creating demo user...")
        existing_user = User.query.filter_by(username='admin').first()
        if not existing_user:
            demo_user = User(
                username='admin',
                email='admin@cyberdefense.local',
                role='admin',
                is_active=True
            )
            demo_user.set_password('password123')
            db.session.add(demo_user)
            db.session.commit()
            print("      ✓ Demo user created")
            print("        Username: admin")
            print("        Password: password123")
        else:
            print("      ✓ Demo user already exists")
        
        # Generate sample dataset
        print("\n[3/4] Generating sample dataset...")
        os.makedirs('data', exist_ok=True)
        DatasetGenerator.generate_dataset(1000, 'data/sample_logs.csv')
        print("      ✓ Sample dataset generated (data/sample_logs.csv)")
        
        # Train ML model
        print("\n[4/4] Training ML models...")
        try:
            trainer = ModelTrainer()
            df = trainer.load_data('data/sample_logs.csv')
            X, y = trainer.preprocess_data(df)
            metrics = trainer.train(X, y)
            trainer.save_model('ml/models/threat_model.pkl')
            print("      ✓ ML model trained successfully")
            print(f"        Accuracy: {metrics['accuracy']:.2%}")
            print(f"        Precision: {metrics['precision']:.2%}")
            print(f"        Recall: {metrics['recall']:.2%}")
            print(f"        F1-Score: {metrics['f1_score']:.2%}")
        except Exception as e:
            print(f"      ⚠ Model training skipped: {e}")
    
    print("\n" + "="*60)
    print("✓ Setup completed successfully!")
    print("="*60)
    print("\n🚀 Start the application:")
    print("   python app.py")
    print("\n📊 Open in browser:")
    print("   http://localhost:5000")
    print("\n🔐 Demo Credentials:")
    print("   Username: admin")
    print("   Password: password123")
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    setup()

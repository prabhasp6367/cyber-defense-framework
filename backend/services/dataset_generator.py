"""Dataset Generation for Training"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DatasetGenerator:
    """Generate synthetic cybersecurity dataset for training"""
    
    @staticmethod
    def generate_dataset(n_samples=5000, output_file='data/training_data.csv'):
        """Generate synthetic cybersecurity logs
        
        Args:
            n_samples: Number of samples to generate
            output_file: Output CSV file path
        """
        print(f"Generating {n_samples} synthetic security logs...")
        
        data = []
        normal_count = int(n_samples * 0.7)  # 70% normal
        suspicious_count = n_samples - normal_count  # 30% suspicious
        
        # Generate normal activity (label=0)
        for i in range(normal_count):
            record = DatasetGenerator._generate_normal_log()
            data.append(record)
        
        # Generate suspicious activity (label=1)
        for i in range(suspicious_count):
            record = DatasetGenerator._generate_suspicious_log()
            data.append(record)
        
        # Shuffle data
        random.shuffle(data)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Save to CSV
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False)
        print(f"Dataset saved to {output_file}")
        
        return df
    
    @staticmethod
    def _generate_normal_log():
        """Generate normal activity log"""
        return {
            'timestamp': (datetime.utcnow() - timedelta(hours=random.randint(0, 168))).isoformat(),
            'source_ip': f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",
            'destination_ip': f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}",
            'source_port': random.randint(1024, 65535),
            'destination_port': random.choice([22, 80, 443, 3389, 5432, 3306]),
            'protocol': random.choice(['TCP', 'UDP', 'ICMP']),
            'event_type': random.choice(['Normal Login', 'HTTP Request', 'DNS Query', 'HTTPS Connection']),
            'bytes_transferred': random.randint(100, 100000),
            'packets': random.randint(10, 500),
            'login_attempts': random.randint(0, 3),
            'failed_logins': random.randint(0, 1),
            'status': 'success',
            'label': 0  # Normal
        }
    
    @staticmethod
    def _generate_suspicious_log():
        """Generate suspicious activity log"""
        threat_type = random.choice([
            'brute_force',
            'port_scan',
            'data_exfiltration',
            'malware',
            'privilege_escalation'
        ])
        
        if threat_type == 'brute_force':
            return {
                'timestamp': (datetime.utcnow() - timedelta(hours=random.randint(0, 168))).isoformat(),
                'source_ip': f"203.0.113.{random.randint(1, 254)}",  # Suspicious IP range
                'destination_ip': f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}",
                'source_port': random.randint(1024, 65535),
                'destination_port': random.choice([22, 3389]),
                'protocol': 'TCP',
                'event_type': 'Multiple Failed Login',
                'bytes_transferred': random.randint(1000, 50000),
                'packets': random.randint(100, 1000),
                'login_attempts': random.randint(15, 100),
                'failed_logins': random.randint(12, 95),
                'status': 'failed',
                'label': 1  # Suspicious
            }
        
        elif threat_type == 'port_scan':
            return {
                'timestamp': (datetime.utcnow() - timedelta(hours=random.randint(0, 168))).isoformat(),
                'source_ip': f"203.0.113.{random.randint(1, 254)}",
                'destination_ip': f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}",
                'source_port': random.randint(1024, 65535),
                'destination_port': random.randint(1, 65535),
                'protocol': 'TCP',
                'event_type': 'Port Scan',
                'bytes_transferred': random.randint(100, 10000),
                'packets': random.randint(500, 5000),
                'login_attempts': 0,
                'failed_logins': 0,
                'status': 'pending',
                'label': 1  # Suspicious
            }
        
        elif threat_type == 'data_exfiltration':
            return {
                'timestamp': (datetime.utcnow() - timedelta(hours=random.randint(0, 168))).isoformat(),
                'source_ip': f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}",
                'destination_ip': f"203.0.113.{random.randint(1, 254)}",
                'source_port': random.randint(1024, 65535),
                'destination_port': random.choice([80, 443, 8080]),
                'protocol': 'TCP',
                'event_type': 'Possible Data Exfiltration',
                'bytes_transferred': random.randint(10000000, 100000000),  # Large transfer
                'packets': random.randint(5000, 50000),
                'login_attempts': 0,
                'failed_logins': 0,
                'status': 'success',
                'label': 1  # Suspicious
            }
        
        elif threat_type == 'malware':
            return {
                'timestamp': (datetime.utcnow() - timedelta(hours=random.randint(0, 168))).isoformat(),
                'source_ip': f"203.0.113.{random.randint(1, 254)}",
                'destination_ip': f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}",
                'source_port': random.randint(1024, 65535),
                'destination_port': random.choice([445, 135, 139]),  # SMB ports
                'protocol': 'TCP',
                'event_type': 'Suspicious Request',
                'bytes_transferred': random.randint(50000, 500000),
                'packets': random.randint(1000, 10000),
                'login_attempts': random.randint(5, 20),
                'failed_logins': random.randint(3, 15),
                'status': 'failed',
                'label': 1  # Suspicious
            }
        
        else:  # privilege_escalation
            return {
                'timestamp': (datetime.utcnow() - timedelta(hours=random.randint(0, 168))).isoformat(),
                'source_ip': f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}",
                'destination_ip': f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}",
                'source_port': random.randint(1024, 65535),
                'destination_port': 445,  # SMB
                'protocol': 'TCP',
                'event_type': 'Brute Force Pattern',
                'bytes_transferred': random.randint(10000, 100000),
                'packets': random.randint(500, 5000),
                'login_attempts': random.randint(20, 50),
                'failed_logins': random.randint(15, 45),
                'status': 'failed',
                'label': 1  # Suspicious
            }

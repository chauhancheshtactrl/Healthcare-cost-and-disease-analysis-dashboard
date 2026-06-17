"""
Generate sample healthcare dataset for analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_healthcare_data(n_records=1000, seed=42):
    """
    Generate synthetic healthcare dataset with realistic patterns
    
    Parameters:
    -----------
    n_records : int
        Number of patient records to generate
    seed : int
        Random seed for reproducibility
        
    Returns:
    --------
    pd.DataFrame
        Healthcare dataset
    """
    
    np.random.seed(seed)
    
    # Define diseases and their characteristics
    diseases = {
        'Diabetes': {'cost_range': (5000, 25000), 'stay_range': (2, 7)},
        'Hypertension': {'cost_range': (3000, 15000), 'stay_range': (1, 4)},
        'Pneumonia': {'cost_range': (8000, 30000), 'stay_range': (3, 10)},
        'Heart Disease': {'cost_range': (15000, 50000), 'stay_range': (5, 14)},
        'Cancer': {'cost_range': (30000, 100000), 'stay_range': (7, 21)},
        'Asthma': {'cost_range': (2000, 12000), 'stay_range': (1, 5)},
        'Depression': {'cost_range': (4000, 20000), 'stay_range': (2, 8)},
        'Arthritis': {'cost_range': (3000, 18000), 'stay_range': (1, 6)},
        'COPD': {'cost_range': (10000, 35000), 'stay_range': (4, 12)},
        'Kidney Disease': {'cost_range': (12000, 40000), 'stay_range': (4, 10)}
    }
    
    data = []
    
    for patient_id in range(1, n_records + 1):
        # Select random disease
        disease = np.random.choice(list(diseases.keys()))
        disease_params = diseases[disease]
        
        # Generate patient attributes
        age = np.random.normal(loc=55, scale=20)
        age = np.clip(age, 18, 95).astype(int)
        
        # Generate treatment cost (with some age correlation)
        cost_min, cost_max = disease_params['cost_range']
        age_factor = 1 + (age - 40) * 0.005  # Age increases cost
        cost_base = np.random.uniform(cost_min, cost_max)
        treatment_cost = int(cost_base * age_factor)
        
        # Generate hospital stay (with age correlation)
        stay_min, stay_max = disease_params['stay_range']
        stay_base = np.random.uniform(stay_min, stay_max)
        hospital_stay_days = int(stay_base * (1 + (age - 40) * 0.01))
        hospital_stay_days = max(1, hospital_stay_days)
        
        data.append({
            'Patient ID': patient_id,
            'Disease': disease,
            'Treatment Cost': treatment_cost,
            'Hospital Stay Days': hospital_stay_days,
            'Age': age
        })
    
    df = pd.DataFrame(data)
    
    return df


if __name__ == "__main__":
    # Generate and save sample data
    df = generate_healthcare_data(n_records=1000)
    
    # Save to CSV
    df.to_csv('healthcare_data.csv', index=False)
    print(f"✅ Generated {len(df)} patient records")
    print(f"\nDataset Preview:")
    print(df.head(10))
    print(f"\nDataset Info:")
    print(df.info())
    print(f"\nBasic Statistics:")
    print(df.describe())

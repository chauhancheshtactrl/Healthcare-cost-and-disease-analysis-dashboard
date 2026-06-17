"""Data loading and preprocessing module for healthcare data"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple


class HealthcareDataLoader:
    """
    Handles loading and initial preprocessing of healthcare data.
    
    This class is responsible for:
    - Loading CSV data
    - Data validation
    - Basic cleaning
    """
    
    def __init__(self, file_path: str):
        """Initialize the data loader.
        
        Args:
            file_path: Path to the CSV file containing healthcare data
        """
        self.file_path = Path(file_path)
        self.data = None
        
    def load(self) -> pd.DataFrame:
        """Load healthcare data from CSV file.
        
        Returns:
            DataFrame with healthcare data
            
        Raises:
            FileNotFoundError: If the data file doesn't exist
            ValueError: If the file format is invalid
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.file_path}")
        
        try:
            self.data = pd.read_csv(self.file_path)
            print(f"✓ Successfully loaded {len(self.data)} records")
            return self.data
        except Exception as e:
            raise ValueError(f"Error loading CSV file: {str(e)}")
    
    def validate(self) -> bool:
        """Validate the integrity of loaded data.
        
        Checks for:
        - Required columns
        - Data types
        - Missing values
        
        Returns:
            True if data is valid
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load() first.")
        
        required_columns = {
            'Patient ID',
            'Disease',
            'Treatment Cost',
            'Hospital Stay Days',
            'Age'
        }
        
        missing_columns = required_columns - set(self.data.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Check for missing values
        missing_count = self.data.isnull().sum()
        if missing_count.any():
            print(f"⚠ Warning: Missing values detected:\n{missing_count[missing_count > 0]}")
        
        # Validate numeric columns
        numeric_issues = []
        if (self.data['Treatment Cost'] < 0).any():
            numeric_issues.append("Negative treatment costs found")
        if (self.data['Hospital Stay Days'] < 0).any():
            numeric_issues.append("Negative hospital stay days found")
        if (self.data['Age'] < 0).any() or (self.data['Age'] > 150).any():
            numeric_issues.append("Invalid age values found")
        
        if numeric_issues:
            print(f"⚠ Validation warnings: {'; '.join(numeric_issues)}")
        
        print("✓ Data validation completed")
        return True
    
    def get_data(self) -> pd.DataFrame:
        """Get the loaded data.
        
        Returns:
            DataFrame with healthcare data
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load() first.")
        return self.data

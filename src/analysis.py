"""Core analysis module for healthcare cost and disease analysis"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class CostAnalysis:
    """Container for cost analysis results"""
    total_cost: float
    average_cost: float
    median_cost: float
    std_dev: float
    min_cost: float
    max_cost: float


class HealthcareAnalyzer:
    """
    Main analyzer for healthcare cost and disease data.
    
    Performs comprehensive analysis including:
    - Cost analysis by disease
    - Treatment patterns
    - Disease statistics
    - Correlation analysis
    """
    
    def __init__(self, data: pd.DataFrame):
        """Initialize the analyzer.
        
        Args:
            data: DataFrame with healthcare data
        """
        self.data = data
        self.disease_stats = None
        self.cost_stats = None
        
    def analyze_cost_by_disease(self) -> pd.DataFrame:
        """Analyze treatment costs by disease.
        
        Returns:
            DataFrame with cost statistics per disease
        """
        analysis = self.data.groupby('Disease').agg({
            'Treatment Cost': ['count', 'sum', 'mean', 'median', 'std', 'min', 'max'],
            'Hospital Stay Days': 'mean',
            'Age': 'mean'
        }).round(2)
        
        # Flatten column names
        analysis.columns = [
            'Patient Count',
            'Total Cost',
            'Average Cost',
            'Median Cost',
            'Cost Std Dev',
            'Min Cost',
            'Max Cost',
            'Avg Hospital Days',
            'Avg Age'
        ]
        
        # Sort by average cost descending
        analysis = analysis.sort_values('Average Cost', ascending=False)
        
        self.disease_stats = analysis
        return analysis
    
    def get_most_expensive_diseases(self, top_n: int = 5) -> pd.DataFrame:
        """Get the most expensive diseases by average treatment cost.
        
        Args:
            top_n: Number of diseases to return
            
        Returns:
            DataFrame with top N most expensive diseases
        """
        if self.disease_stats is None:
            self.analyze_cost_by_disease()
        
        return self.disease_stats.head(top_n)[['Average Cost', 'Patient Count', 'Total Cost']]
    
    def get_cost_efficiency_metrics(self) -> pd.DataFrame:
        """Calculate cost efficiency: cost per hospital day.
        
        Returns:
            DataFrame with cost efficiency metrics by disease
        """
        efficiency = self.data.groupby('Disease').apply(
            lambda x: pd.Series({
                'Cost per Hospital Day': (x['Treatment Cost'] / x['Hospital Stay Days']).mean(),
                'Patient Count': len(x),
                'Avg Cost': x['Treatment Cost'].mean(),
                'Avg Hospital Days': x['Hospital Stay Days'].mean()
            })
        ).round(2)
        
        return efficiency.sort_values('Cost per Hospital Day', ascending=False)
    
    def get_age_based_analysis(self) -> Dict:
        """Analyze treatment costs by age groups.
        
        Returns:
            Dictionary with age-based analysis
        """
        age_bins = [0, 18, 35, 50, 65, 100]
        age_labels = ['0-17', '18-34', '35-49', '50-64', '65+']
        
        self.data['Age Group'] = pd.cut(self.data['Age'], bins=age_bins, labels=age_labels)
        
        age_analysis = self.data.groupby('Age Group').agg({
            'Treatment Cost': ['count', 'mean', 'sum'],
            'Hospital Stay Days': 'mean'
        }).round(2)
        
        age_analysis.columns = ['Patient Count', 'Average Cost', 'Total Cost', 'Avg Hospital Days']
        
        return age_analysis
    
    def get_disease_hospital_stay_analysis(self) -> pd.DataFrame:
        """Analyze hospital stay patterns by disease.
        
        Returns:
            DataFrame with hospital stay statistics
        """
        hospital_analysis = self.data.groupby('Disease').agg({
            'Hospital Stay Days': ['mean', 'median', 'max', 'min'],
            'Treatment Cost': 'mean',
            'Patient ID': 'count'
        }).round(2)
        
        hospital_analysis.columns = [
            'Avg Hospital Days',
            'Median Hospital Days',
            'Max Hospital Days',
            'Min Hospital Days',
            'Avg Treatment Cost',
            'Total Patients'
        ]
        
        return hospital_analysis.sort_values('Avg Hospital Days', ascending=False)
    
    def get_correlation_analysis(self) -> pd.DataFrame:
        """Analyze correlations between numeric variables.
        
        Returns:
            Correlation matrix
        """
        numeric_cols = ['Treatment Cost', 'Hospital Stay Days', 'Age']
        correlation = self.data[numeric_cols].corr().round(3)
        return correlation
    
    def generate_summary_statistics(self) -> Dict:
        """Generate overall summary statistics.
        
        Returns:
            Dictionary with summary statistics
        """
        return {
            'Total Patients': len(self.data),
            'Total Treatment Cost': self.data['Treatment Cost'].sum(),
            'Average Treatment Cost': self.data['Treatment Cost'].mean(),
            'Median Treatment Cost': self.data['Treatment Cost'].median(),
            'Min Treatment Cost': self.data['Treatment Cost'].min(),
            'Max Treatment Cost': self.data['Treatment Cost'].max(),
            'Average Hospital Stay (days)': self.data['Hospital Stay Days'].mean(),
            'Average Patient Age': self.data['Age'].mean(),
            'Total Unique Diseases': self.data['Disease'].nunique()
        }

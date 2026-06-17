"""
Healthcare Cost Analysis Module
Performs comprehensive cost analysis by disease, demographics, and other factors
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, List


class HealthcareCostAnalyzer:
    """Analyze healthcare costs and disease patterns"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize analyzer with healthcare dataset
        
        Parameters:
        -----------
        df : pd.DataFrame
            Healthcare dataset with columns: Patient ID, Disease, Treatment Cost, 
            Hospital Stay Days, Age
        """
        self.df = df.copy()
        self.validate_data()
    
    def validate_data(self):
        """Validate dataset structure and content"""
        required_columns = ['Patient ID', 'Disease', 'Treatment Cost', 'Hospital Stay Days', 'Age']
        missing_cols = [col for col in required_columns if col not in self.df.columns]
        
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Check for null values
        if self.df.isnull().any().any():
            print("⚠️  Warning: Dataset contains null values")
    
    # ==================== COST ANALYSIS ====================
    
    def cost_by_disease(self) -> pd.DataFrame:
        """
        Analyze total and average treatment costs by disease
        
        Returns:
        --------
        pd.DataFrame
            Cost statistics by disease
        """
        cost_stats = self.df.groupby('Disease').agg({
            'Treatment Cost': ['sum', 'mean', 'median', 'std', 'min', 'max', 'count']
        }).round(2)
        
        cost_stats.columns = ['Total Cost', 'Average Cost', 'Median Cost', 
                               'Std Dev', 'Min Cost', 'Max Cost', 'Patient Count']
        
        cost_stats = cost_stats.sort_values('Total Cost', ascending=False)
        cost_stats['% of Total'] = (cost_stats['Total Cost'] / cost_stats['Total Cost'].sum() * 100).round(2)
        
        return cost_stats
    
    def most_expensive_diseases(self, top_n: int = 5) -> pd.DataFrame:
        """
        Get top N most expensive diseases by total and average cost
        
        Parameters:
        -----------
        top_n : int
            Number of top diseases to return
            
        Returns:
        --------
        pd.DataFrame
            Top expensive diseases
        """
        cost_summary = self.df.groupby('Disease').agg({
            'Treatment Cost': ['sum', 'mean', 'count']
        }).round(2)
        
        cost_summary.columns = ['Total Cost', 'Average Cost', 'Patient Count']
        cost_summary = cost_summary.sort_values('Total Cost', ascending=False).head(top_n)
        
        return cost_summary
    
    def average_treatment_cost(self) -> Dict:
        """
        Calculate average treatment costs overall and by demographics
        
        Returns:
        --------
        Dict
            Average cost statistics
        """
        stats = {
            'Overall Average': self.df['Treatment Cost'].mean(),
            'Median': self.df['Treatment Cost'].median(),
            'Std Dev': self.df['Treatment Cost'].std(),
            'Min': self.df['Treatment Cost'].min(),
            'Max': self.df['Treatment Cost'].max(),
            'Total': self.df['Treatment Cost'].sum()
        }
        
        return {k: round(v, 2) for k, v in stats.items()}
    
    # ==================== DEMOGRAPHICS ANALYSIS ====================
    
    def cost_by_age_group(self) -> pd.DataFrame:
        """
        Analyze costs by age groups
        
        Returns:
        --------
        pd.DataFrame
            Cost statistics by age group
        """
        # Create age groups
        age_bins = [0, 30, 40, 50, 60, 70, 100]
        age_labels = ['18-30', '31-40', '41-50', '51-60', '61-70', '70+']
        
        self.df['Age Group'] = pd.cut(self.df['Age'], bins=age_bins, labels=age_labels)
        
        age_stats = self.df.groupby('Age Group', observed=True).agg({
            'Treatment Cost': ['mean', 'median', 'count', 'sum'],
            'Hospital Stay Days': 'mean'
        }).round(2)
        
        age_stats.columns = ['Avg Cost', 'Median Cost', 'Patient Count', 'Total Cost', 'Avg Stay Days']
        
        return age_stats
    
    # ==================== HOSPITAL STAY ANALYSIS ====================
    
    def stay_cost_correlation(self) -> Tuple[float, pd.DataFrame]:
        """
        Analyze relationship between hospital stay and treatment cost
        
        Returns:
        --------
        Tuple[float, pd.DataFrame]
            Correlation coefficient and statistics by stay duration
        """
        correlation = self.df['Hospital Stay Days'].corr(self.df['Treatment Cost'])
        
        # Categorize by stay duration
        stay_bins = [0, 3, 7, 14, 100]
        stay_labels = ['Short (1-3)', 'Medium (4-7)', 'Long (8-14)', 'Very Long (14+)']
        self.df['Stay Category'] = pd.cut(self.df['Hospital Stay Days'], 
                                          bins=stay_bins, labels=stay_labels)
        
        stay_stats = self.df.groupby('Stay Category', observed=True).agg({
            'Treatment Cost': ['mean', 'median', 'count'],
            'Hospital Stay Days': 'mean'
        }).round(2)
        
        stay_stats.columns = ['Avg Cost', 'Median Cost', 'Patient Count', 'Avg Days']
        
        return correlation, stay_stats
    
    # ==================== DISEASE BURDEN ANALYSIS ====================
    
    def disease_prevalence(self) -> pd.DataFrame:
        """
        Analyze disease prevalence and burden
        
        Returns:
        --------
        pd.DataFrame
            Disease statistics
        """
        prevalence = self.df.groupby('Disease').agg({
            'Patient ID': 'count',
            'Treatment Cost': 'mean',
            'Hospital Stay Days': 'mean',
            'Age': 'mean'
        }).round(2)
        
        prevalence.columns = ['Patient Count', 'Avg Cost', 'Avg Stay Days', 'Avg Age']
        prevalence['% of Patients'] = (prevalence['Patient Count'] / prevalence['Patient Count'].sum() * 100).round(2)
        prevalence = prevalence.sort_values('Patient Count', ascending=False)
        
        return prevalence
    
    # ==================== COST-EFFICIENCY ANALYSIS ====================
    
    def cost_efficiency_metrics(self) -> pd.DataFrame:
        """
        Calculate cost-efficiency metrics by disease
        Cost per day of hospital stay
        
        Returns:
        --------
        pd.DataFrame
            Efficiency metrics
        """
        efficiency = self.df.groupby('Disease').agg({
            'Treatment Cost': 'mean',
            'Hospital Stay Days': 'mean'
        }).round(2)
        
        efficiency.columns = ['Avg Cost', 'Avg Stay Days']
        efficiency['Cost per Day'] = (efficiency['Avg Cost'] / efficiency['Avg Stay Days']).round(2)
        efficiency = efficiency.sort_values('Cost per Day', ascending=False)
        
        return efficiency
    
    # ==================== OUTLIER ANALYSIS ====================
    
    def identify_outliers(self, std_threshold: float = 2.5) -> pd.DataFrame:
        """
        Identify cost outliers using statistical methods
        
        Parameters:
        -----------
        std_threshold : float
            Number of standard deviations to define outliers
            
        Returns:
        --------
        pd.DataFrame
            Outlier cases
        """
        mean_cost = self.df['Treatment Cost'].mean()
        std_cost = self.df['Treatment Cost'].std()
        
        outliers = self.df[
            (self.df['Treatment Cost'] > mean_cost + std_threshold * std_cost) |
            (self.df['Treatment Cost'] < mean_cost - std_threshold * std_cost)
        ].copy()
        
        outliers = outliers.sort_values('Treatment Cost', ascending=False)
        
        return outliers
    
    # ==================== SUMMARY STATISTICS ====================
    
    def generate_summary_report(self) -> Dict:
        """
        Generate comprehensive summary statistics
        
        Returns:
        --------
        Dict
            Summary report
        """
        report = {
            'Total Patients': len(self.df),
            'Total Diseases': self.df['Disease'].nunique(),
            'Total Healthcare Expenditure': f"${self.df['Treatment Cost'].sum():,.2f}",
            'Average Cost per Patient': f"${self.df['Treatment Cost'].mean():,.2f}",
            'Median Cost': f"${self.df['Treatment Cost'].median():,.2f}",
            'Average Hospital Stay': f"{self.df['Hospital Stay Days'].mean():.1f} days",
            'Average Patient Age': f"{self.df['Age'].mean():.1f} years",
            'Most Common Disease': self.df['Disease'].value_counts().index[0],
            'Most Expensive Disease': self.df.groupby('Disease')['Treatment Cost'].mean().idxmax(),
            'Lowest Cost Disease': self.df.groupby('Disease')['Treatment Cost'].mean().idxmin()
        }
        
        return report


if __name__ == "__main__":
    # Example usage
    from data.generate_sample_data import generate_healthcare_data
    
    # Generate sample data
    df = generate_healthcare_data(n_records=1000)
    
    # Initialize analyzer
    analyzer = HealthcareCostAnalyzer(df)
    
    # Perform analysis
    print("=" * 60)
    print("HEALTHCARE COST ANALYSIS SUMMARY")
    print("=" * 60)
    
    # Summary statistics
    summary = analyzer.generate_summary_report()
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    print("\n" + "=" * 60)
    print("COST BY DISEASE")
    print("=" * 60)
    print(analyzer.cost_by_disease())
    
    print("\n" + "=" * 60)
    print("DISEASE PREVALENCE")
    print("=" * 60)
    print(analyzer.disease_prevalence())

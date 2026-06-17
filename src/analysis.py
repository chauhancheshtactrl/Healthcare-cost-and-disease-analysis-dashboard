"""Core analysis functions for healthcare cost and disease analysis."""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
from src.data_loader import load_config


def calculate_cost_statistics(df: pd.DataFrame, config: Dict[str, Any] = None) -> pd.DataFrame:
    """
    Calculate comprehensive cost statistics by disease.
    
    Parameters
    ----------
    df : pd.DataFrame
        Healthcare dataset
    config : dict, optional
        Configuration dictionary
    
    Returns
    -------
    pd.DataFrame
        Cost statistics by disease
    """
    if config is None:
        config = load_config()
    
    cols = config['columns']
    disease_col = cols['disease']
    cost_col = cols['treatment_cost']
    days_col = cols['hospital_days']
    
    cost_stats = df.groupby(disease_col).agg({
        cost_col: [
            ('Total Cost', 'sum'),
            ('Average Cost', 'mean'),
            ('Median Cost', 'median'),
            ('Std Dev', 'std'),
            ('Min Cost', 'min'),
            ('Max Cost', 'max'),
            ('Patient Count', 'count'),
        ],
        days_col: [
            ('Avg Hospital Days', 'mean'),
        ]
    }).round(2)
    
    # Flatten column names
    cost_stats.columns = [col[1] if col[1] else col[0] for col in cost_stats.columns]
    
    # Calculate additional metrics
    cost_stats['Cost per Hospital Day'] = (
        cost_stats['Total Cost'] / (cost_stats['Avg Hospital Days'] * cost_stats['Patient Count'])
    ).round(2)
    
    return cost_stats.sort_values('Average Cost', ascending=False)


def get_disease_ranking(df: pd.DataFrame, config: Dict[str, Any] = None) -> pd.DataFrame:
    """
    Rank diseases by total and average treatment costs.
    
    Parameters
    ----------
    df : pd.DataFrame
        Healthcare dataset
    config : dict, optional
        Configuration dictionary
    
    Returns
    -------
    pd.DataFrame
        Diseases ranked by cost
    """
    if config is None:
        config = load_config()
    
    cols = config['columns']
    disease_col = cols['disease']
    cost_col = cols['treatment_cost']
    
    ranking = df.groupby(disease_col)[cost_col].agg([
        ('Total Cost', 'sum'),
        ('Average Cost', 'mean'),
        ('Median Cost', 'median'),
        ('Patient Count', 'count'),
    ]).round(2)
    
    # Create rank columns
    ranking['Rank by Total Cost'] = ranking['Total Cost'].rank(ascending=False, method='min').astype(int)
    ranking['Rank by Average Cost'] = ranking['Average Cost'].rank(ascending=False, method='min').astype(int)
    
    return ranking.sort_values('Rank by Total Cost')


def calculate_efficiency_metrics(df: pd.DataFrame, config: Dict[str, Any] = None) -> pd.DataFrame:
    """
    Calculate healthcare efficiency metrics by disease.
    
    Parameters
    ----------
    df : pd.DataFrame
        Healthcare dataset
    config : dict, optional
        Configuration dictionary
    
    Returns
    -------
    pd.DataFrame
        Efficiency metrics
    """
    if config is None:
        config = load_config()
    
    cols = config['columns']
    disease_col = cols['disease']
    cost_col = cols['treatment_cost']
    days_col = cols['hospital_days']
    
    efficiency = df.groupby(disease_col).agg({
        cost_col: ['sum', 'mean'],
        days_col: ['sum', 'mean'],
    })
    
    # Flatten columns
    efficiency.columns = ['Total Cost', 'Avg Cost', 'Total Days', 'Avg Days']
    
    # Calculate efficiency metrics
    efficiency['Cost per Day'] = (efficiency['Total Cost'] / efficiency['Total Days']).round(2)
    efficiency['Days per Patient'] = efficiency['Avg Days'].round(2)
    efficiency['Patient Count'] = df.groupby(disease_col).size()
    
    return efficiency.sort_values('Avg Cost', ascending=False)


def get_top_diseases(df: pd.DataFrame, metric: str = 'cost', top_n: int = 10, 
                     config: Dict[str, Any] = None) -> List[Tuple[str, float]]:
    """
    Get top diseases by specified metric.
    
    Parameters
    ----------
    df : pd.DataFrame
        Healthcare dataset
    metric : str
        'cost', 'cases', or 'days'
    top_n : int
        Number of top diseases to return
    config : dict, optional
        Configuration dictionary
    
    Returns
    -------
    List[Tuple[str, float]]
        List of (disease, value) tuples
    """
    if config is None:
        config = load_config()
    
    cols = config['columns']
    disease_col = cols['disease']
    cost_col = cols['treatment_cost']
    days_col = cols['hospital_days']
    
    if metric == 'cost':
        top = df.groupby(disease_col)[cost_col].sum().nlargest(top_n)
    elif metric == 'cases':
        top = df.groupby(disease_col).size().nlargest(top_n)
    elif metric == 'days':
        top = df.groupby(disease_col)[days_col].sum().nlargest(top_n)
    else:
        raise ValueError(f"Unknown metric: {metric}")
    
    return list(zip(top.index, top.values))


def calculate_demographics_analysis(df: pd.DataFrame, config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Analyze disease prevalence by age group and demographics.
    
    Parameters
    ----------
    df : pd.DataFrame
        Healthcare dataset
    config : dict, optional
        Configuration dictionary
    
    Returns
    -------
    dict
        Demographic analysis results
    """
    if config is None:
        config = load_config()
    
    cols = config['columns']
    age_col = cols['age']
    disease_col = cols['disease']
    cost_col = cols['treatment_cost']
    
    # Create age groups
    df_temp = df.copy()
    df_temp['Age Group'] = pd.cut(df_temp[age_col], 
                                   bins=[0, 18, 35, 50, 65, 100],
                                   labels=['0-18', '19-35', '36-50', '51-65', '65+'])
    
    analysis = {
        'age_distribution': df.groupby(age_col).size().to_dict(),
        'avg_cost_by_age_group': df_temp.groupby('Age Group')[cost_col].mean().round(2).to_dict(),
        'disease_by_age_group': df_temp.groupby(['Age Group', disease_col]).size().unstack(fill_value=0).to_dict(),
    }
    
    return analysis


def generate_key_insights(df: pd.DataFrame, config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generate key insights from healthcare data.
    
    Parameters
    ----------
    df : pd.DataFrame
        Healthcare dataset
    config : dict, optional
        Configuration dictionary
    
    Returns
    -------
    dict
        Key insights
    """
    if config is None:
        config = load_config()
    
    cols = config['columns']
    cost_col = cols['treatment_cost']
    days_col = cols['hospital_days']
    disease_col = cols['disease']
    
    # Calculate key metrics
    total_cost = df[cost_col].sum()
    avg_cost = df[cost_col].mean()
    max_disease = df.groupby(disease_col)[cost_col].sum().idxmax()
    max_disease_cost = df.groupby(disease_col)[cost_col].sum().max()
    
    insights = {
        'total_healthcare_cost': round(total_cost, 2),
        'average_treatment_cost': round(avg_cost, 2),
        'total_patients': len(df),
        'unique_diseases': df[disease_col].nunique(),
        'most_expensive_disease': max_disease,
        'most_expensive_disease_cost': round(max_disease_cost, 2),
        'average_hospital_days': round(df[days_col].mean(), 2),
        'total_hospital_days': df[days_col].sum(),
        'cost_per_hospital_day': round(total_cost / df[days_col].sum(), 2),
        'diseases': get_top_diseases(df, 'cost', 5, config),
    }
    
    return insights
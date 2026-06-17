"""Data loading and preprocessing utilities for healthcare dataset."""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Any
import yaml


def load_config(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def load_healthcare_data(filepath: str) -> pd.DataFrame:
    """
    Load healthcare data from CSV file.
    
    Parameters
    ----------
    filepath : str
        Path to the CSV file
    
    Returns
    -------
    pd.DataFrame
        Loaded healthcare data
    """
    try:
        df = pd.read_csv(filepath)
        print(f"✓ Data loaded successfully: {filepath}")
        print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        print(f"✗ File not found: {filepath}")
        raise
    except Exception as e:
        print(f"✗ Error loading file: {str(e)}")
        raise


def validate_data(df: pd.DataFrame, config: Dict[str, Any]) -> Tuple[bool, list]:
    """
    Validate healthcare dataset structure and content.
    
    Parameters
    ----------
    df : pd.DataFrame
        Healthcare dataset
    config : dict
        Configuration dictionary with column names
    
    Returns
    -------
    Tuple[bool, list]
        (is_valid, list_of_errors)
    """
    errors = []
    cols = config['columns']
    required_cols = [cols['patient_id'], cols['disease'], 
                     cols['treatment_cost'], cols['hospital_days'], cols['age']]
    
    # Check required columns exist
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing columns: {missing_cols}")
    
    # Check data types
    if cols['patient_id'] in df.columns:
        if not pd.api.types.is_integer_dtype(df[cols['patient_id']]):
            errors.append(f"{cols['patient_id']} should be integer")
    
    if cols['treatment_cost'] in df.columns:
        if not pd.api.types.is_numeric_dtype(df[cols['treatment_cost']]):
            errors.append(f"{cols['treatment_cost']} should be numeric")
    
    if cols['hospital_days'] in df.columns:
        if not pd.api.types.is_integer_dtype(df[cols['hospital_days']]):
            errors.append(f"{cols['hospital_days']} should be integer")
    
    if cols['age'] in df.columns:
        if not pd.api.types.is_integer_dtype(df[cols['age']]):
            errors.append(f"{cols['age']} should be integer")
    
    return len(errors) == 0, errors


def clean_data(df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """
    Clean and preprocess healthcare data.
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw healthcare dataset
    config : dict
        Configuration dictionary
    
    Returns
    -------
    pd.DataFrame
        Cleaned dataset
    """
    df_clean = df.copy()
    cols = config['columns']
    
    print("\nData Cleaning Steps:")
    
    # Remove duplicates
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    print(f"✓ Removed {initial_rows - len(df_clean)} duplicate rows")
    
    # Handle missing values
    missing_before = df_clean.isnull().sum().sum()
    if missing_before > 0:
        print(f"✓ Found {missing_before} missing values")
        # For numeric columns, fill with median
        numeric_cols = [cols['treatment_cost'], cols['hospital_days'], cols['age']]
        for col in numeric_cols:
            if col in df_clean.columns and df_clean[col].isnull().sum() > 0:
                df_clean[col].fillna(df_clean[col].median(), inplace=True)
        # For categorical columns, fill with mode
        if cols['disease'] in df_clean.columns:
            df_clean[cols['disease']].fillna(df_clean[cols['disease']].mode()[0], inplace=True)
    
    # Remove negative values in cost and days
    df_clean = df_clean[df_clean[cols['treatment_cost']] > 0]
    df_clean = df_clean[df_clean[cols['hospital_days']] > 0]
    df_clean = df_clean[df_clean[cols['age']] > 0]
    
    print(f"✓ Removed records with invalid values")
    print(f"✓ Final dataset shape: {df_clean.shape[0]} rows × {df_clean.shape[1]} columns")
    
    return df_clean


def get_data_summary(df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate data summary statistics.
    
    Parameters
    ----------
    df : pd.DataFrame
        Healthcare dataset
    config : dict
        Configuration dictionary
    
    Returns
    -------
    dict
        Summary statistics
    """
    cols = config['columns']
    
    summary = {
        'total_records': len(df),
        'total_patients': df[cols['patient_id']].nunique(),
        'unique_diseases': df[cols['disease']].nunique(),
        'disease_list': sorted(df[cols['disease']].unique().tolist()),
        'age_range': (df[cols['age']].min(), df[cols['age']].max()),
        'cost_range': (df[cols['treatment_cost']].min(), df[cols['treatment_cost']].max()),
        'hospital_days_range': (df[cols['hospital_days']].min(), df[cols['hospital_days']].max()),
    }
    
    return summary
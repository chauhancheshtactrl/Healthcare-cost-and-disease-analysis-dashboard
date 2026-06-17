"""Visualization functions for healthcare cost and disease analysis."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, Any, List, Tuple
from src.data_loader import load_config
from src.analysis import (
    calculate_cost_statistics,
    get_top_diseases,
    calculate_efficiency_metrics,
)


def setup_plot_style():
    """Setup matplotlib and seaborn styling."""
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10


def plot_cost_by_disease(df: pd.DataFrame, config: Dict[str, Any] = None, 
                         top_n: int = 10, figsize: Tuple[int, int] = (14, 8)) -> plt.Figure:
    """
    Create bar chart of average treatment cost by disease.
    
    Parameters
    ----------
    df : pd.DataFrame
        Healthcare dataset
    config : dict, optional
        Configuration dictionary
    top_n : int
        Number of top diseases to display
    figsize : tuple
        Figure size
    
    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    if config is None:
        config = load_config()
    
    cols = config['columns']
    cost_stats = calculate_cost_statistics(df, config)
    top_diseases = cost_stats.head(top_n)
    
    fig, ax = plt.subplots(figsize=figsize)
    bars = ax.barh(range(len(top_diseases)), top_diseases['Average Cost'], color='steelblue')
    ax.set_yticks(range(len(top_diseases)))
    ax.set_yticklabels(top_diseases.index)
    ax.set_xlabel('Average Treatment Cost ($)', fontsize=12, fontweight='bold')
    ax.set_title(f'Top {top_n} Most Expensive Diseases by Average Cost', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.invert_yaxis()
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, 
                f'${bar.get_width():,.0f}', ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    return fig


def plot_disease_cost_distribution(df: pd.DataFrame, config: Dict[str, Any] = None,
                                   figsize: Tuple[int, int] = (14, 8)) -> plt.Figure:
    """
    Create pie chart of total cost distribution by disease.
    
    Parameters
    ----------
    df : pd.DataFrame
        Healthcare dataset
    config : dict, optional
        Configuration dictionary
    figsize : tuple
        Figure size
    
    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    if config is None:
        config = load_config()
    
    cols = config['columns']
    disease_col = cols['disease']
    cost_col = cols['treatment_cost']
    
    cost_by_disease = df.groupby(disease_col)[cost_col].sum().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=figsize)
    colors = plt.cm.Set3(np.linspace(0, 1, len(cost_by_disease)))
    wedges, texts, autotexts = ax.pie(cost_by_disease.values, labels=cost_by_disease.index,
                                        autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title('Total Healthcare Cost Distribution by Disease', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Enhance text readability
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.tight_layout()
    return fig


def plot_hospital_stay_vs_cost(df: pd.DataFrame, config: Dict[str, Any] = None,
                               figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
    """
    Create scatter plot of hospital stay days vs treatment cost.
    
    Parameters
    ----------
    df : pd.DataFrame
        Healthcare dataset
    config : dict, optional
        Configuration dictionary
    figsize : tuple
        Figure size
    
    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    if config is None:
        config = load_config()
    
    cols = config['columns']
    days_col = cols['hospital_days']
    cost_col = cols['treatment_cost']
    disease_col = cols['disease']
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot scatter with disease colors
    diseases = df[disease_col].unique()
    colors = plt.cm.tab20(np.linspace(0, 1, len(diseases)))
    
    for disease, color in zip(diseases, colors):
        disease_data = df[df[disease_col] == disease]
        ax.scatter(disease_data[days_col], disease_data[cost_col], 
                   label=disease, alpha=0.6, s=50, color=color)
    
    ax.set_xlabel('Hospital Stay Days', fontsize=12, fontweight='bold')
    ax.set_ylabel('Treatment Cost ($)', fontsize=12, fontweight='bold')
    ax.set_title('Relationship: Hospital Stay Duration vs Treatment Cost', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_cost_distribution_boxplot(df: pd.DataFrame, config: Dict[str, Any] = None,
                                   figsize: Tuple[int, int] = (14, 8)) -> plt.Figure:
    """
    Create box plot of cost distribution by disease.
    
    Parameters
    ----------
    df : pd.DataFrame
        Healthcare dataset
    config : dict, optional
        Configuration dictionary
    figsize : tuple
        Figure size
    
    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    if config is None:
        config = load_config()
    
    cols = config['columns']
    disease_col = cols['disease']
    cost_col = cols['treatment_cost']
    
    # Sort diseases by median cost
    disease_order = df.groupby(disease_col)[cost_col].median().sort_values(ascending=False).index
    
    fig, ax = plt.subplots(figsize=figsize)
    sns.boxplot(data=df, x=disease_col, y=cost_col, order=disease_order, ax=ax, palette='Set2')
    ax.set_xlabel('Disease', fontsize=12, fontweight='bold')
    ax.set_ylabel('Treatment Cost ($)', fontsize=12, fontweight='bold')
    ax.set_title('Treatment Cost Distribution by Disease', fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    return fig


def create_interactive_dashboard(df: pd.DataFrame, config: Dict[str, Any] = None) -> go.Figure:
    """
    Create interactive Plotly dashboard.
    
    Parameters
    ----------
    df : pd.DataFrame
        Healthcare dataset
    config : dict, optional
        Configuration dictionary
    
    Returns
    -------
    go.Figure
        Plotly figure
    """
    if config is None:
        config = load_config()
    
    cols = config['columns']
    cost_col = cols['treatment_cost']
    disease_col = cols['disease']
    days_col = cols['hospital_days']
    age_col = cols['age']
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Average Cost by Disease", "Total Cost Distribution",
                       "Cost vs Hospital Days", "Patient Count by Disease"),
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "scatter"}, {"type": "bar"}]]
    )
    
    # 1. Average cost by disease (top 10)
    top_diseases_cost = df.groupby(disease_col)[cost_col].mean().nlargest(10).sort_values()
    fig.add_trace(
        go.Bar(y=top_diseases_cost.index, x=top_diseases_cost.values, 
               orientation='h', marker_color='steelblue', name='Avg Cost'),
        row=1, col=1
    )
    
    # 2. Total cost by disease (pie)
    cost_by_disease = df.groupby(disease_col)[cost_col].sum()
    fig.add_trace(
        go.Pie(labels=cost_by_disease.index, values=cost_by_disease.values, name='Total Cost'),
        row=1, col=2
    )
    
    # 3. Scatter plot: cost vs days
    fig.add_trace(
        go.Scatter(x=df[days_col], y=df[cost_col], mode='markers',
                   marker=dict(size=5, color=df[age_col], colorscale='Viridis', 
                              showscale=True, colorbar=dict(title="Age")),
                   name='Patients'),
        row=2, col=1
    )
    
    # 4. Patient count by disease (top 10)
    patient_count = df.groupby(disease_col).size().nlargest(10).sort_values()
    fig.add_trace(
        go.Bar(y=patient_count.index, x=patient_count.values, 
               orientation='h', marker_color='coral', name='Patient Count'),
        row=2, col=2
    )
    
    # Update layout
    fig.update_xaxes(title_text="Average Cost ($)", row=1, col=1)
    fig.update_xaxes(title_text="Hospital Stay Days", row=2, col=1)
    fig.update_xaxes(title_text="Patient Count", row=2, col=2)
    
    fig.update_yaxes(title_text="Disease", row=1, col=1)
    fig.update_yaxes(title_text="Cost ($)", row=2, col=1)
    fig.update_yaxes(title_text="Disease", row=2, col=2)
    
    fig.update_layout(height=900, title_text="Healthcare Cost and Disease Analysis Dashboard",
                     showlegend=True)
    
    return fig


def create_dashboard(df: pd.DataFrame, config: Dict[str, Any] = None,
                     output_path: str = None) -> Dict[str, Any]:
    """
    Create all visualizations for the dashboard.
    
    Parameters
    ----------
    df : pd.DataFrame
        Healthcare dataset
    config : dict, optional
        Configuration dictionary
    output_path : str, optional
        Path to save dashboard
    
    Returns
    -------
    dict
        Dictionary of all figures
    """
    if config is None:
        config = load_config()
    
    setup_plot_style()
    
    figures = {
        'cost_by_disease': plot_cost_by_disease(df, config),
        'cost_distribution': plot_disease_cost_distribution(df, config),
        'cost_vs_hospital_days': plot_hospital_stay_vs_cost(df, config),
        'cost_boxplot': plot_cost_distribution_boxplot(df, config),
        'interactive_dashboard': create_interactive_dashboard(df, config),
    }
    
    return figures
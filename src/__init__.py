"""Healthcare Cost and Disease Analysis Package"""

__version__ = "1.0.0"
__author__ = "Healthcare Data Analytics Team"

from src.data_loader import load_healthcare_data
from src.analysis import (
    calculate_cost_statistics,
    get_disease_ranking,
    calculate_efficiency_metrics,
)
from src.visualization import create_dashboard

__all__ = [
    'load_healthcare_data',
    'calculate_cost_statistics',
    'get_disease_ranking',
    'calculate_efficiency_metrics',
    'create_dashboard',
]
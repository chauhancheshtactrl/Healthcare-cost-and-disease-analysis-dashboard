# Healthcare Cost and Disease Analysis Dashboard

## Project Overview

This data analysis project examines healthcare expenditure patterns and disease burdens using patient-level hospital data. It provides actionable insights for healthcare administrators and decision-makers through comprehensive cost analysis, statistical insights, and interactive visualizations.

## Objectives

- **Cost Analysis**: Analyze treatment costs by disease and identify cost drivers
- **Healthcare Economics**: Understand cost-disease relationships and resource allocation
- **Patient Demographics**: Examine disease prevalence and hospital stay patterns
- **Business Intelligence**: Generate executive summaries for healthcare decision-makers

## Dataset

The analysis uses patient-level hospital data with the following columns:

| Column | Description | Data Type |
|--------|-------------|----------|
| Patient ID | Unique patient identifier | Integer |
| Disease | Medical condition/diagnosis | String |
| Treatment Cost | Cost of treatment in USD | Float |
| Hospital Stay Days | Duration of hospitalization | Integer |
| Age | Patient age in years | Integer |

## Project Structure

```
├── data/
│   ├── raw/                          # Raw input data
│   └── processed/                    # Cleaned and processed data
├── notebooks/
│   ├── 01_data_exploration.ipynb     # EDA and data quality checks
│   ├── 02_cost_analysis.ipynb        # Detailed cost analysis
│   └── 03_executive_summary.ipynb    # Executive summary generation
├── src/
│   ├── __init__.py
│   ├── data_loader.py                # Data loading utilities
│   ├── analysis.py                   # Analysis functions
│   └── visualization.py              # Visualization functions
├── reports/
│   ├── executive_summary.html        # Executive summary report
│   ├── cost_analysis_report.html     # Detailed cost analysis
│   └── charts/                       # Generated visualizations
├── requirements.txt                   # Python dependencies
├── config.yaml                        # Configuration settings
└── README.md                          # This file
```

## Key Analyses

### 1. Cost Analysis by Disease
- Total treatment costs per disease
- Average treatment cost by disease
- Cost distribution statistics
- Cost per hospital stay day

### 2. Most Expensive Diseases
- Ranking diseases by total and average treatment costs
- Identification of high-cost diseases
- Cost drivers and contributing factors

### 3. Healthcare Utilization
- Average hospital stay duration by disease
- Patient age distribution by disease
- Hospital stay cost efficiency analysis

### 4. Executive Insights
- Key performance indicators (KPIs)
- Cost trends and patterns
- Resource allocation recommendations
- Healthcare expenditure summary

## Visualizations

The project includes interactive charts and dashboards:

- **Bar Charts**: Average treatment cost by disease
- **Pie Charts**: Cost distribution across diseases
- **Box Plots**: Treatment cost distributions
- **Scatter Plots**: Relationship between hospital days and treatment cost
- **Heatmaps**: Cross-disease analysis matrices
- **Dashboard**: Interactive executive summary dashboard

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- scipy

Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/chauhancheshtactrl/Healthcare-cost-and-disease-analysis-dashboard.git
   cd Healthcare-cost-and-disease-analysis-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Place your data**
   - Add your CSV file to `data/raw/`
   - Update `config.yaml` with the correct filename

4. **Run analysis**
   ```bash
   jupyter notebook notebooks/01_data_exploration.ipynb
   ```

5. **Generate reports**
   ```bash
   python -m src.generate_reports
   ```

## Usage Examples

### Basic Data Loading
```python
from src.data_loader import load_healthcare_data

df = load_healthcare_data('data/raw/healthcare_data.csv')
print(df.head())
print(df.describe())
```

### Cost Analysis
```python
from src.analysis import calculate_cost_statistics

cost_by_disease = calculate_cost_statistics(df)
print(cost_by_disease)
```

### Generate Visualizations
```python
from src.visualization import create_dashboard

figs = create_dashboard(df)
# Save and display visualizations
```

## Key Insights Generated

The analysis provides:

1. **Cost Rankings**: Which diseases are most expensive?
2. **Efficiency Metrics**: Cost per hospital day for each disease
3. **Demographic Insights**: Age patterns and disease prevalence
4. **Resource Utilization**: Average hospital stays and treatment patterns
5. **Recommendations**: Evidence-based insights for healthcare planning

## Target Audience

- Healthcare Business Analysts
- Health Economics Professionals
- Hospital Administrators
- Healthcare Policy Makers
- Data Analysis Professionals in Healthcare

## Reports Generated

1. **Executive Summary Report**: High-level insights for decision-makers
2. **Cost Analysis Report**: Detailed cost breakdowns and trends
3. **Statistical Analysis**: Descriptive statistics and distributions
4. **Interactive Dashboard**: Visual exploration of healthcare data

## Future Enhancements

- Predictive modeling for cost forecasting
- Seasonal trend analysis
- Interactive web-based dashboard with Dash/Streamlit
- Machine learning for disease cost prediction
- Time-series analysis for longitudinal studies

## Author

Created for healthcare data analysis and business intelligence applications.

## License

MIT License - See LICENSE file for details
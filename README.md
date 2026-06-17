# Healthcare Cost and Disease Analysis Dashboard

A comprehensive Python-based analysis and visualization system for healthcare cost and disease data, designed for healthcare business analysts and health economics professionals.

## Project Overview

This project provides a complete analytics pipeline for examining healthcare treatment costs, disease patterns, and healthcare utilization metrics. It combines data analysis, statistical insights, and interactive visualizations to support evidence-based healthcare decision-making.

### Key Features

- **Cost Analysis**: Comprehensive analysis of treatment costs by disease, including averages, medians, and trends
- **Disease Comparison**: Statistical comparison of disease burden and cost metrics
- **Hospital Stay Analysis**: Examination of length of stay patterns and their relationship to costs
- **Age-Based Insights**: Analysis of healthcare costs and utilization across age groups
- **Cost Efficiency Metrics**: Calculation of cost per hospital day to identify efficiency opportunities
- **Interactive Visualizations**: Professional Plotly-based charts and dashboards
- **Executive Reports**: HTML and text-based executive summary reports

## Dataset

The analysis uses a healthcare dataset with the following columns:

| Column | Description | Type |
|--------|-------------|------|
| Patient ID | Unique patient identifier | String |
| Disease | Primary diagnosis | Categorical |
| Treatment Cost | Total treatment cost in USD | Numeric |
| Hospital Stay Days | Number of days hospitalized | Numeric |
| Age | Patient age in years | Numeric |

## Project Structure

```
Healthcare-cost-and-disease-analysis-dashboard/
├── data/
│   └── sample_healthcare_data.csv          # Sample dataset
├── src/
│   ├── __init__.py
│   ├── data_loader.py                      # Data loading and validation
│   ├── analysis.py                         # Core analysis logic
│   ├── visualizations.py                   # Chart generation
│   └── reporting.py                        # Executive report generation
├── reports/                                # Output directory for visualizations and reports
├── main.py                                 # Main execution script
├── requirements.txt                        # Python dependencies
└── README.md                               # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/chauhancheshtactrl/Healthcare-cost-and-disease-analysis-dashboard.git
cd Healthcare-cost-and-disease-analysis-dashboard
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Analysis

```bash
python main.py
```

This command will:
1. Load and validate the healthcare dataset
2. Perform comprehensive analysis
3. Generate interactive visualizations
4. Create executive summary reports

### Output

The analysis generates the following outputs in the `reports/` directory:

#### Visualizations (Interactive HTML)
- `cost_by_disease.html` - Average treatment cost comparison by disease
- `total_cost_by_disease.html` - Total treatment cost burden by disease
- `disease_distribution.html` - Patient distribution across diseases (pie chart)
- `hospital_stay_analysis.html` - Hospital stay patterns by disease
- `cost_efficiency.html` - Cost efficiency metrics (cost per hospital day)
- `age_cost_scatter.html` - Scatter plot of treatment cost vs. patient age
- `correlation_heatmap.html` - Correlation matrix of key variables

#### Reports
- `executive_summary.html` - Professional HTML executive summary report
- `executive_summary.txt` - Text-based executive summary report

## Analysis Components

### 1. Data Loader (`src/data_loader.py`)

Handles data loading, validation, and initial preprocessing:
- CSV file reading
- Data integrity validation
- Missing value detection
- Numeric data validation

### 2. Analysis Module (`src/analysis.py`)

Performs comprehensive healthcare analytics:
- **Cost Analysis by Disease**: Aggregate statistics on treatment costs
- **Cost Efficiency**: Cost per hospital day calculations
- **Age-Based Analysis**: Healthcare costs across age groups
- **Hospital Stay Analysis**: Length of stay patterns
- **Correlation Analysis**: Relationships between variables
- **Summary Statistics**: Overall dataset metrics

Key Methods:
- `analyze_cost_by_disease()` - Disease-level cost statistics
- `get_most_expensive_diseases()` - Top N costly diseases
- `get_cost_efficiency_metrics()` - Cost per day analysis
- `get_age_based_analysis()` - Age group breakdown
- `get_disease_hospital_stay_analysis()` - Hospital stay patterns
- `get_correlation_analysis()` - Variable correlations

### 3. Visualizations (`src/visualizations.py`)

Creates professional, interactive Plotly-based visualizations:
- Bar charts for cost comparisons
- Pie charts for distribution analysis
- Scatter plots for relationship analysis
- Heatmaps for correlation analysis

All visualizations are interactive and include hover tooltips for detailed information.

### 4. Executive Reporting (`src/reporting.py`)

Generates comprehensive reports in multiple formats:
- **HTML Report**: Professional, styled report with tables and key findings
- **Text Report**: Formatted text report for documentation

Reports include:
- Executive summary
- Key performance indicators
- Detailed findings by disease and age group
- Strategic recommendations
- Links to interactive visualizations

## Key Metrics and Analysis

### Cost Metrics
- **Total Treatment Cost**: Sum of all treatment costs
- **Average Treatment Cost**: Mean cost per patient
- **Median Treatment Cost**: Midpoint of cost distribution
- **Cost Range**: Minimum and maximum treatment costs

### Efficiency Metrics
- **Cost per Hospital Day**: Average treatment cost divided by hospital stay length
- **Cost Efficiency Ranking**: Diseases ranked by cost-effectiveness

### Utilization Metrics
- **Average Hospital Stay**: Mean days hospitalized by disease and age group
- **Patient Distribution**: Count and percentage of patients per disease
- **Age Demographics**: Patient population by age group

### Correlation Analysis
- Relationships between treatment cost, hospital stay, and age
- Statistical significance of correlations

## Career Applications

This project is specifically designed to demonstrate skills valuable for:

### Healthcare Business Analyst Roles
- **Data Analysis**: Comprehensive analysis of healthcare costs and utilization
- **Financial Metrics**: Cost analysis, efficiency calculations, and trend identification
- **Reporting**: Executive-level insights and recommendations
- **Decision Support**: Data-driven insights for healthcare management

### Health Economics Roles
- **Cost-Effectiveness Analysis**: Cost per outcome analysis
- **Healthcare Utilization**: Hospital stay patterns and disease burden
- **Resource Allocation**: Data-driven recommendations for budget allocation
- **Economic Modeling**: Foundation for comparative cost analysis

### Skills Demonstrated
- **Python Programming**: Data manipulation with pandas, numpy
- **Data Analysis**: Descriptive statistics, correlation analysis
- **Data Visualization**: Professional charts with Plotly and Matplotlib
- **Business Intelligence**: Executive reporting and insights
- **Healthcare Domain Knowledge**: Understanding of cost drivers and utilization metrics

## Customization

### Using Your Own Data

Replace `data/sample_healthcare_data.csv` with your own dataset. Ensure it contains:
- Patient ID
- Disease
- Treatment Cost
- Hospital Stay Days
- Age

### Configuration

You can customize the analysis by modifying:
- Age bins in `src/analysis.py`
- Visualization styles in `src/visualizations.py`
- Report templates in `src/reporting.py`

## Requirements

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Static visualizations
- **seaborn**: Statistical visualizations
- **plotly**: Interactive visualizations
- **scipy**: Statistical functions

## License

This project is provided as-is for educational and professional use.

## Contact & Support

For questions or improvements, please visit the project repository:
https://github.com/chauhancheshtactrl/Healthcare-cost-and-disease-analysis-dashboard

---

**Professional Summary**: This project represents a complete analytical solution for healthcare cost and disease analysis, combining data science, business intelligence, and healthcare domain expertise. It demonstrates proficiency in Python-based data analysis, visualization, and executive reporting—key competencies for healthcare business analyst and health economics positions.

"""
Main analysis notebook runner
Orchestrates data generation, analysis, visualization, and reporting
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Add scripts to path
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'data')

from generate_sample_data import generate_healthcare_data
from healthcare_analyzer import HealthcareCostAnalyzer
from visualizations import HealthcareVisualizer
from report_generator import ExecutiveSummaryReport, generate_html_report


def ensure_directories():
    """Ensure all required directories exist"""
    directories = ['data', 'reports', 'visualizations', 'scripts']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_subsection(title):
    """Print formatted subsection header"""
    print(f"\n{'─' * 80}")
    print(f"  {title}")
    print(f"{'─' * 80}\n")


def main():
    """Main execution function"""
    
    print_section("HEALTHCARE COST AND DISEASE ANALYSIS")
    print("Starting comprehensive healthcare analysis project...")
    
    # 1. ENSURE DIRECTORIES
    print_subsection("Step 1: Setting Up Directories")
    ensure_directories()
    print("✅ All directories created")
    
    # 2. GENERATE DATA
    print_subsection("Step 2: Generating Synthetic Healthcare Data")
    print("Generating 1000 patient records with realistic disease patterns...")
    df = generate_healthcare_data(n_records=1000)
    print(f"✅ Generated {len(df):,} patient records")
    print(f"\nDataset Shape: {df.shape}")
    print(f"Columns: {', '.join(df.columns)}")
    print(f"\nFirst 5 records:\n{df.head()}")
    
    # Save dataset
    data_path = 'data/healthcare_data.csv'
    df.to_csv(data_path, index=False)
    print(f"\n✅ Dataset saved to: {data_path}")
    
    # 3. INITIALIZE ANALYZER
    print_subsection("Step 3: Analyzing Healthcare Costs and Disease Patterns")
    analyzer = HealthcareCostAnalyzer(df)
    
    # Summary Report
    print("\n📊 SUMMARY STATISTICS:")
    summary = analyzer.generate_summary_report()
    for key, value in summary.items():
        print(f"  {key:<30} {value}")
    
    # Cost Analysis
    print_subsection("3.1 Cost Analysis by Disease")
    cost_by_disease = analyzer.cost_by_disease()
    print(cost_by_disease)
    
    # Most Expensive Diseases
    print_subsection("3.2 Top 5 Most Expensive Diseases")
    expensive = analyzer.most_expensive_diseases(top_n=5)
    print(expensive)
    
    # Average Treatment Cost
    print_subsection("3.3 Average Treatment Cost Statistics")
    avg_cost = analyzer.average_treatment_cost()
    for key, value in avg_cost.items():
        print(f"  {key:<25} ${value:>12,.2f}")
    
    # Disease Prevalence
    print_subsection("3.4 Disease Prevalence Analysis")
    prevalence = analyzer.disease_prevalence()
    print(prevalence)
    
    # Cost by Age Group
    print_subsection("3.5 Cost Analysis by Age Group")
    age_costs = analyzer.cost_by_age_group()
    print(age_costs)
    
    # Cost-Stay Correlation
    print_subsection("3.6 Hospital Stay and Cost Analysis")
    correlation, stay_stats = analyzer.stay_cost_correlation()
    print(f"Correlation between hospital stay and treatment cost: {correlation:.3f}")
    print(f"\nCost by Hospital Stay Duration:\n{stay_stats}")
    
    # Cost Efficiency
    print_subsection("3.7 Cost Efficiency Metrics (Cost per Day of Stay)")
    efficiency = analyzer.cost_efficiency_metrics()
    print(efficiency)
    
    # Outlier Analysis
    print_subsection("3.8 Outlier Analysis (High-Cost Cases)")
    outliers = analyzer.identify_outliers(std_threshold=2.5)
    print(f"Found {len(outliers)} outlier cases")
    print(f"\nTop 10 Most Expensive Cases:\n{outliers.head(10)}")
    
    # 4. CREATE VISUALIZATIONS
    print_subsection("Step 4: Creating Visualizations and Dashboards")
    print("Generating comprehensive charts and dashboards...")
    
    viz = HealthcareVisualizer(df)
    
    viz.plot_cost_by_disease('visualizations/01_cost_by_disease.png')
    viz.plot_average_cost_by_disease('visualizations/02_avg_cost_by_disease.png')
    viz.plot_disease_prevalence('visualizations/03_disease_prevalence.png')
    viz.plot_cost_vs_stay('visualizations/04_cost_vs_stay.png')
    viz.plot_cost_by_age_group('visualizations/05_cost_by_age_group.png')
    viz.plot_disease_cost_heatmap('visualizations/06_disease_heatmap.png')
    viz.create_executive_dashboard('visualizations/07_executive_dashboard.png')
    
    print("\n✅ All visualizations created successfully!")
    
    # 5. GENERATE REPORTS
    print_subsection("Step 5: Generating Executive Summary Reports")
    
    # Text Report
    report_gen = ExecutiveSummaryReport(df, analyzer)
    txt_report_path = 'reports/executive_summary.txt'
    report_gen.generate_report(txt_report_path)
    
    # HTML Report
    html_report_path = 'reports/executive_summary.html'
    generate_html_report(df, html_report_path)
    
    # 6. FINAL SUMMARY
    print_section("ANALYSIS COMPLETE")
    print("""
📁 PROJECT STRUCTURE:
  
  ├── data/
  │   ├── healthcare_data.csv              ← Dataset (1000 patient records)
  │   └── generate_sample_data.py         ← Data generation script
  │
  ├── scripts/
  │   ├── healthcare_analyzer.py          ← Cost analysis module
  │   ├── visualizations.py               ← Chart generation
  │   ├── report_generator.py             ← Report generation
  │   └── main.py                         ← Main orchestration script
  │
  ├── visualizations/
  │   ├── 01_cost_by_disease.png          ← Total cost by disease
  │   ├── 02_avg_cost_by_disease.png      ← Average cost by disease
  │   ├── 03_disease_prevalence.png       ← Disease prevalence pie chart
  │   ├── 04_cost_vs_stay.png             ← Cost vs hospital stay scatter
  │   ├── 05_cost_by_age_group.png        ← Cost by age group boxplot
  │   ├── 06_disease_heatmap.png          ← Disease statistics heatmap
  │   └── 07_executive_dashboard.png      ← Comprehensive dashboard
  │
  ├── reports/
  │   ├── executive_summary.txt           ← Detailed text report
  │   └── executive_summary.html          ← Professional HTML report
  │
  └── README.md                           ← Project documentation
    """)
    
    print("\n📊 KEY DELIVERABLES:")
    print(f"  ✅ Healthcare dataset: {data_path}")
    print(f"  ✅ Analysis results: 7+ visualizations in visualizations/")
    print(f"  ✅ Text report: {txt_report_path}")
    print(f"  ✅ HTML report: {html_report_path}")
    
    print("\n💼 SUITABLE FOR:")
    print("  • Healthcare Business Analyst job applications")
    print("  • Health Economics positions")
    print("  • Healthcare Management roles")
    print("  • Data-driven healthcare decision-making")
    
    print("\n" + "=" * 80)
    print("Analysis pipeline completed successfully! 🎉")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()

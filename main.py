#!/usr/bin/env python3
"""
Main execution script for Healthcare Cost and Disease Analysis Dashboard

This script orchestrates the complete analysis pipeline:
1. Data loading and validation
2. Comprehensive analysis
3. Visualization generation
4. Executive report generation

Usage:
    python main.py
"""

import os
from pathlib import Path
from src.data_loader import HealthcareDataLoader
from src.analysis import HealthcareAnalyzer
from src.visualizations import HealthcareVisualizer
from src.reporting import ExecutiveReportGenerator


def create_output_directories():
    """Create necessary output directories."""
    Path('reports').mkdir(exist_ok=True)
    print("✓ Output directories ready")


def main():
    """
    Execute the complete healthcare analysis pipeline.
    """
    print("\n" + "="*80)
    print("HEALTHCARE COST AND DISEASE ANALYSIS DASHBOARD")
    print("="*80 + "\n")
    
    # Setup
    create_output_directories()
    
    # 1. LOAD DATA
    print("[1/5] Loading data...")
    loader = HealthcareDataLoader('data/sample_healthcare_data.csv')
    data = loader.load()
    loader.validate()
    print()
    
    # 2. ANALYZE DATA
    print("[2/5] Performing analysis...")
    analyzer = HealthcareAnalyzer(data)
    
    disease_stats = analyzer.analyze_cost_by_disease()
    print(f"✓ Analyzed {len(disease_stats)} diseases")
    
    top_diseases = analyzer.get_most_expensive_diseases(top_n=5)
    print(f"✓ Identified top 5 most expensive diseases")
    
    cost_efficiency = analyzer.get_cost_efficiency_metrics()
    print(f"✓ Calculated cost efficiency metrics")
    
    age_analysis = analyzer.get_age_based_analysis()
    print(f"✓ Completed age-based analysis")
    
    hospital_analysis = analyzer.get_disease_hospital_stay_analysis()
    print(f"✓ Analyzed hospital stay patterns")
    
    correlation = analyzer.get_correlation_analysis()
    print(f"✓ Generated correlation analysis")
    
    summary_stats = analyzer.generate_summary_statistics()
    print()
    
    # 3. CREATE VISUALIZATIONS
    print("[3/5] Creating visualizations...")
    visualizer = HealthcareVisualizer()
    
    visualizer.create_cost_by_disease_chart(disease_stats)
    visualizer.create_disease_distribution_chart(data)
    visualizer.create_total_cost_by_disease_chart(disease_stats)
    visualizer.create_hospital_stay_analysis(hospital_analysis)
    visualizer.create_cost_efficiency_chart(cost_efficiency)
    visualizer.create_age_cost_scatter(data)
    visualizer.create_correlation_heatmap(correlation)
    print()
    
    # 4. GENERATE REPORTS
    print("[4/5] Generating reports...")
    analysis_results = {
        'summary_statistics': summary_stats,
        'disease_statistics': disease_stats,
        'top_diseases': top_diseases,
        'age_analysis': age_analysis,
        'hospital_analysis': hospital_analysis
    }
    
    report_generator = ExecutiveReportGenerator(analysis_results)
    report_generator.generate_html_report()
    report_generator.generate_text_report()
    print()
    
    # 5. SUMMARY
    print("[5/5] Summary Statistics")
    print("-" * 80)
    print(f"Total Patients Analyzed:        {int(summary_stats['Total Patients']):,}")
    print(f"Total Treatment Cost:           ${summary_stats['Total Treatment Cost']:,.0f}")
    print(f"Average Treatment Cost:         ${summary_stats['Average Treatment Cost']:,.0f}")
    print(f"Median Treatment Cost:          ${summary_stats['Median Treatment Cost']:,.0f}")
    print(f"Average Hospital Stay:          {summary_stats['Average Hospital Stay (days)']:.1f} days")
    print(f"Average Patient Age:            {summary_stats['Average Patient Age']:.1f} years")
    print(f"Total Unique Diseases:          {int(summary_stats['Total Unique Diseases'])}")
    print("-" * 80)
    print()
    
    # Print top diseases
    print("TOP 5 MOST EXPENSIVE DISEASES:")
    print("-" * 80)
    for idx, (disease, row) in enumerate(top_diseases.iterrows(), 1):
        print(f"{idx}. {disease:<20} ${row['Average Cost']:>12,.0f} avg  "
              f"({int(row['Patient Count']):>3} patients, "
              f"${row['Total Cost']:>12,.0f} total)")
    print()
    
    print("="*80)
    print("✓ ANALYSIS COMPLETE")
    print("="*80)
    print("\nGenerated Files:")
    print("  📊 Visualizations in: ./reports/")
    print("  📄 HTML Report: ./reports/executive_summary.html")
    print("  📋 Text Report: ./reports/executive_summary.txt")
    print("\nNext Steps:")
    print("  1. Review the executive summary reports in the reports/ directory")
    print("  2. Open interactive HTML visualizations in your browser")
    print("  3. Use insights for healthcare business analysis and decision-making")
    print()


if __name__ == '__main__':
    main()

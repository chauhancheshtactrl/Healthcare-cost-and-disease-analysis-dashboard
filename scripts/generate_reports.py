"""
Report Generation Script
Generates comprehensive analysis reports with all visualizations
"""

import pandas as pd
import sys
import os
from pathlib import Path
import yaml

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import load_healthcare_data
from src.visualization import HealthcareVisualizer, save_figures


def load_config():
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def generate_all_reports(df, config, output_path='reports/charts/'):
    """Generate all charts and reports"""
    
    # Extract column names and settings from config
    cost_col = config['columns']['treatment_cost']
    disease_col = config['columns']['disease']
    hospital_col = config['columns']['hospital_days']
    age_col = config['columns']['age']
    
    # Initialize visualizer
    viz = HealthcareVisualizer(
        style=config['visualization']['style'],
        palette=config['visualization']['color_palette'],
        dpi=config['visualization']['figure_dpi']
    )
    
    print("🎨 Generating visualizations...")
    figures = {}
    
    # 1. Cost Analysis Charts
    print("  ✓ Generating cost by disease bar chart...")
    figures['01_cost_by_disease'] = viz.plot_cost_by_disease_bar(df, cost_col, disease_col)
    
    print("  ✓ Generating cost distribution box plot...")
    figures['02_cost_distribution'] = viz.plot_cost_distribution_boxplot(df, cost_col, disease_col)
    
    print("  ✓ Generating cost pie chart...")
    figures['03_cost_distribution_pie'] = viz.plot_cost_pie_chart(df, cost_col, disease_col)
    
    # 2. Hospital Stay Analysis
    print("  ✓ Generating hospital days analysis...")
    figures['04_hospital_days'] = viz.plot_hospital_days_by_disease(df, hospital_col, disease_col)
    
    # 3. Cost vs Hospital Days
    print("  ✓ Generating cost vs hospital days scatter plot...")
    figures['05_cost_vs_hospital'] = viz.plot_cost_vs_hospital_days_scatter(df, cost_col, hospital_col, disease_col)
    
    # 4. Age Analysis
    print("  ✓ Generating age distribution analysis...")
    figures['06_age_distribution'] = viz.plot_age_distribution_by_disease(df, age_col, disease_col)
    
    # 5. Heatmap
    print("  ✓ Generating heatmap...")
    figures['07_heatmap_cost_age'] = viz.plot_heatmap_cost_by_age_disease(df, cost_col, age_col, disease_col)
    
    # 6. Cost Efficiency
    print("  ✓ Generating cost efficiency chart...")
    figures['08_cost_efficiency'] = viz.plot_cost_efficiency(df, cost_col, hospital_col, disease_col)
    
    # 7. Statistical Summary
    print("  ✓ Generating statistical summary...")
    figures['09_statistical_summary'] = viz.plot_statistical_summary(df, cost_col, disease_col)
    
    # 8. Interactive Charts
    print("  ✓ Generating interactive dashboard...")
    figures['10_interactive_dashboard'] = viz.create_interactive_dashboard(df, cost_col, disease_col, hospital_col, age_col)
    
    print("  ✓ Generating interactive cost analysis...")
    figures['11_interactive_cost_analysis'] = viz.create_interactive_cost_analysis(df, cost_col, disease_col)
    
    print("  ✓ Generating 3D scatter plot...")
    figures['12_interactive_3d_scatter'] = viz.create_interactive_scatter_3d(df, cost_col, hospital_col, age_col, disease_col)
    
    # Save all figures
    print(f"\n💾 Saving visualizations to {output_path}...")
    save_figures(figures, output_path)
    
    return figures


def generate_html_report(df, config, figures_path='reports/charts/', output_file='reports/dashboard.html'):
    """Generate an HTML dashboard combining all visualizations"""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Healthcare Cost and Disease Analysis Dashboard</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                line-height: 1.6;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }
            
            header {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin-bottom: 30px;
                text-align: center;
            }
            
            h1 {
                color: #667eea;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .subtitle {
                color: #666;
                font-size: 1.1em;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            .stat-value {
                font-size: 2em;
                font-weight: bold;
                margin: 10px 0;
            }
            
            .stat-label {
                font-size: 0.9em;
                opacity: 0.9;
            }
            
            .section {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }
            
            .section h2 {
                color: #667eea;
                margin-bottom: 20px;
                font-size: 1.8em;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }
            
            .chart-container {
                margin: 20px 0;
                text-align: center;
            }
            
            .chart-container img {
                max-width: 100%;
                height: auto;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            iframe {
                width: 100%;
                min-height: 500px;
                border: none;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            footer {
                background: white;
                padding: 20px;
                text-align: center;
                border-radius: 10px;
                margin-top: 30px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🏥 Healthcare Cost and Disease Analysis Dashboard</h1>
                <p class="subtitle">Comprehensive analysis of healthcare expenditure patterns and disease burdens</p>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-label">Total Patients</div>
                        <div class="stat-value">{total_patients:,}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Unique Diseases</div>
                        <div class="stat-value">{num_diseases}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Total Healthcare Cost</div>
                        <div class="stat-value">${total_cost:,.0f}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Average Cost per Patient</div>
                        <div class="stat-value">${avg_cost:,.0f}</div>
                    </div>
                </div>
            </header>
            
            <section class="section">
                <h2>📊 Cost Analysis</h2>
                <div class="chart-container">
                    <img src="charts/01_cost_by_disease.png" alt="Cost by Disease Analysis">
                </div>
                <div class="chart-container">
                    <img src="charts/02_cost_distribution.png" alt="Cost Distribution">
                </div>
                <div class="chart-container">
                    <img src="charts/03_cost_distribution_pie.png" alt="Cost Distribution Pie">
                </div>
            </section>
            
            <section class="section">
                <h2>🏥 Hospital Utilization</h2>
                <div class="chart-container">
                    <img src="charts/04_hospital_days.png" alt="Hospital Days Analysis">
                </div>
                <div class="chart-container">
                    <img src="charts/05_cost_vs_hospital.png" alt="Cost vs Hospital Days">
                </div>
            </section>
            
            <section class="section">
                <h2>👥 Patient Demographics</h2>
                <div class="chart-container">
                    <img src="charts/06_age_distribution.png" alt="Age Distribution">
                </div>
                <div class="chart-container">
                    <img src="charts/07_heatmap_cost_age.png" alt="Cost by Age and Disease">
                </div>
            </section>
            
            <section class="section">
                <h2>⚡ Cost Efficiency Metrics</h2>
                <div class="chart-container">
                    <img src="charts/08_cost_efficiency.png" alt="Cost Efficiency">
                </div>
            </section>
            
            <section class="section">
                <h2>📈 Statistical Summary</h2>
                <div class="chart-container">
                    <img src="charts/09_statistical_summary.png" alt="Statistical Summary">
                </div>
            </section>
            
            <section class="section">
                <h2>🔍 Interactive Visualizations</h2>
                <div class="chart-container">
                    <h3>Healthcare Dashboard (Interactive)</h3>
                    <iframe src="charts/10_interactive_dashboard.html"></iframe>
                </div>
                <div class="chart-container">
                    <h3>Cost Analysis Comparison (Interactive)</h3>
                    <iframe src="charts/11_interactive_cost_analysis.html"></iframe>
                </div>
                <div class="chart-container">
                    <h3>3D Analysis: Cost vs Hospital Days vs Age (Interactive)</h3>
                    <iframe src="charts/12_interactive_3d_scatter.html"></iframe>
                </div>
            </section>
            
            <footer>
                <p>Generated on {timestamp}</p>
                <p>Healthcare Cost and Disease Analysis Dashboard | Data Analysis Report</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    # Calculate statistics
    cost_col = config['columns']['treatment_cost']
    disease_col = config['columns']['disease']
    
    total_patients = len(df)
    num_diseases = df[disease_col].nunique()
    total_cost = df[cost_col].sum()
    avg_cost = df[cost_col].mean()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = html_content.format(
        total_patients=total_patients,
        num_diseases=num_diseases,
        total_cost=total_cost,
        avg_cost=avg_cost,
        timestamp=timestamp
    )
    
    # Save HTML file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"✅ HTML dashboard generated: {output_file}")


def main():
    """Main function to run complete report generation"""
    
    print("📋 Healthcare Cost Analysis - Report Generation\n")
    
    # Load configuration
    print("📖 Loading configuration...")
    config = load_config()
    
    # Load data
    print("📂 Loading healthcare data...")
    data_path = os.path.join(config['data']['raw_path'], config['data']['filename'])
    
    if not os.path.exists(data_path):
        print(f"❌ Error: Data file not found at {data_path}")
        print("   Please add your healthcare data CSV file to data/raw/ directory")
        return
    
    df = load_healthcare_data(data_path)
    print(f"✅ Loaded {len(df):,} records from {config['data']['filename']}")
    
    # Generate visualizations
    output_path = config['output']['charts_path']
    os.makedirs(output_path, exist_ok=True)
    
    figures = generate_all_reports(df, config, output_path)
    print(f"\n✅ All visualizations generated successfully!")
    print(f"📁 Charts saved to: {output_path}")
    
    # Generate HTML report
    print("\n🌐 Generating HTML dashboard...")
    generate_html_report(df, config, output_path, config['output']['dashboard_path'])
    
    print("\n" + "="*60)
    print("✅ REPORT GENERATION COMPLETE!")
    print("="*60)
    print(f"\n📊 View your interactive dashboard:")
    print(f"   Open: {config['output']['dashboard_path']}")
    print(f"\n📈 All charts saved to: {output_path}")
    print("\n✨ Thank you for using Healthcare Analysis Dashboard!")


if __name__ == "__main__":
    main()

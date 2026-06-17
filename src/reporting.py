"""Executive reporting module for healthcare analysis"""

import pandas as pd
from datetime import datetime
from typing import Dict, Any


class ExecutiveReportGenerator:
    """
    Generates professional executive summary reports.
    """
    
    def __init__(self, analysis_results: Dict[str, Any]):
        """Initialize report generator.
        
        Args:
            analysis_results: Dictionary containing all analysis results
        """
        self.analysis_results = analysis_results
        self.report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def generate_html_report(self, output_path: str = 'reports/executive_summary.html') -> None:
        """Generate comprehensive HTML executive summary report.
        
        Args:
            output_path: Path to save the HTML report
        """
        html_content = self._build_html_report()
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        print(f"✓ Saved: {output_path}")
    
    def generate_text_report(self, output_path: str = 'reports/executive_summary.txt') -> None:
        """Generate text-based executive summary report.
        
        Args:
            output_path: Path to save the text report
        """
        text_content = self._build_text_report()
        
        with open(output_path, 'w') as f:
            f.write(text_content)
        
        print(f"✓ Saved: {output_path}")
    
    def _build_html_report(self) -> str:
        """Build HTML report content.
        
        Returns:
            HTML string for the report
        """
        summary = self.analysis_results['summary_statistics']
        disease_stats = self.analysis_results['disease_statistics']
        top_diseases = self.analysis_results['top_diseases']
        age_analysis = self.analysis_results['age_analysis']
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Healthcare Cost and Disease Analysis - Executive Summary</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                    margin-bottom: 5px;
                }}
                h2 {{
                    color: #34495e;
                    margin-top: 30px;
                    margin-bottom: 15px;
                    border-left: 4px solid #3498db;
                    padding-left: 10px;
                }}
                h3 {{
                    color: #7f8c8d;
                    margin-top: 20px;
                }}
                .metadata {{
                    background-color: #ecf0f1;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 30px;
                    font-size: 0.9em;
                }}
                .metrics-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .metric-box {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                .metric-value {{
                    font-size: 1.8em;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .metric-label {{
                    font-size: 0.9em;
                    opacity: 0.9;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    background-color: #f9f9f9;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                    padding: 12px;
                    text-align: left;
                    font-weight: 600;
                }}
                td {{
                    padding: 12px;
                    border-bottom: 1px solid #ddd;
                }}
                tr:hover {{
                    background-color: #f0f0f0;
                }}
                .highlight {{
                    background-color: #fff3cd;
                    padding: 15px;
                    border-left: 4px solid #ffc107;
                    border-radius: 4px;
                    margin: 20px 0;
                }}
                .key-finding {{
                    background-color: #d4edda;
                    border-left: 4px solid #28a745;
                    padding: 15px;
                    margin: 15px 0;
                    border-radius: 4px;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    color: #7f8c8d;
                    font-size: 0.9em;
                }}
                .currency {{
                    color: #27ae60;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Healthcare Cost and Disease Analysis</h1>
                <h2 style="border: none; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-top: 0;">Executive Summary Report</h2>
                
                <div class="metadata">
                    <strong>Report Generated:</strong> {self.report_date}<br>
                    <strong>Data Analysis Period:</strong> Complete Dataset<br>
                    <strong>Total Patients Analyzed:</strong> {int(summary['Total Patients'])}
                </div>
                
                <h2>Key Performance Indicators</h2>
                <div class="metrics-grid">
                    <div class="metric-box">
                        <div class="metric-label">Total Treatment Cost</div>
                        <div class="metric-value"><span class="currency">${summary['Total Treatment Cost']:,.0f}</span></div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Average Cost per Patient</div>
                        <div class="metric-value"><span class="currency">${summary['Average Treatment Cost']:,.0f}</span></div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Median Treatment Cost</div>
                        <div class="metric-value"><span class="currency">${summary['Median Treatment Cost']:,.0f}</span></div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Average Hospital Stay</div>
                        <div class="metric-value">{summary['Average Hospital Stay (days)']:.1f} <span style="font-size: 0.5em;">days</span></div>
                    </div>
                </div>
                
                <h2>Executive Summary</h2>
                <div class="highlight">
                    <p><strong>Overview:</strong> This analysis examines healthcare treatment costs and disease patterns across {int(summary['Total Unique Diseases'])} major disease categories. The dataset reveals significant cost variations across different diseases, with implications for resource allocation and treatment planning.</p>
                </div>
                
                <h2>Key Findings</h2>
                """
        
        # Add key findings
        most_expensive = top_diseases.iloc[0]
        least_expensive = top_diseases.iloc[-1]
        
        html += f"""
                <div class="key-finding">
                    <strong>🔴 Most Expensive Disease:</strong> {top_diseases.index[0]} with an average treatment cost of <span class="currency">${most_expensive['Average Cost']:,.0f}</span> per patient ({int(most_expensive['Patient Count'])} patients)
                </div>
                
                <div class="key-finding">
                    <strong>🟢 Most Cost-Effective Disease:</strong> {top_diseases.index[-1]} with an average treatment cost of <span class="currency">${least_expensive['Average Cost']:,.0f}</span> per patient ({int(least_expensive['Patient Count'])} patients)
                </div>
                
                <div class="key-finding">
                    <strong>📊 Average Patient Age:</strong> {summary['Average Patient Age']:.1f} years, indicating a mixed demographic across the patient population
                </div>
                
                <h2>Cost Analysis by Disease</h2>
                <p>The following table summarizes treatment costs and patient counts across major diseases:</p>
                <table>
                    <tr>
                        <th>Disease</th>
                        <th>Patient Count</th>
                        <th>Average Cost</th>
                        <th>Total Cost</th>
                        <th>Avg Hospital Days</th>
                    </tr>
        """
        
        for disease in disease_stats.index:
            row = disease_stats.loc[disease]
            html += f"""
                    <tr>
                        <td><strong>{disease}</strong></td>
                        <td>{int(row['Patient Count'])}</td>
                        <td><span class="currency">${row['Average Cost']:,.0f}</span></td>
                        <td><span class="currency">${row['Total Cost']:,.0f}</span></td>
                        <td>{row['Avg Hospital Days']:.1f}</td>
                    </tr>
            """
        
        html += """
                </table>
                
                <h2>Age-Based Cost Analysis</h2>
                <p>Analysis of treatment costs across different age groups reveals patterns in disease burden and healthcare utilization:</p>
                <table>
                    <tr>
                        <th>Age Group</th>
                        <th>Patient Count</th>
                        <th>Average Cost</th>
                        <th>Total Cost</th>
                        <th>Avg Hospital Days</th>
                    </tr>
        """
        
        for age_group in age_analysis.index:
            row = age_analysis.loc[age_group]
            html += f"""
                    <tr>
                        <td><strong>{age_group}</strong></td>
                        <td>{int(row['Patient Count'])}</td>
                        <td><span class="currency">${row['Average Cost']:,.0f}</span></td>
                        <td><span class="currency">${row['Total Cost']:,.0f}</span></td>
                        <td>{row['Avg Hospital Days']:.1f}</td>
                    </tr>
            """
        
        html += """
                </table>
                
                <h2>Recommendations</h2>
                <ul>
                    <li><strong>Resource Allocation:</strong> Prioritize resource allocation toward high-cost, high-volume diseases for maximum impact on healthcare economics.</li>
                    <li><strong>Treatment Optimization:</strong> Investigate treatment protocols for diseases with high cost-per-day ratios to identify efficiency improvements.</li>
                    <li><strong>Preventive Care:</strong> Emphasize preventive care strategies for age groups with increasing disease burden and treatment costs.</li>
                    <li><strong>Hospital Stay Reduction:</strong> Target diseases with longer average hospital stays for care pathway optimization.</li>
                </ul>
                
                <h2>Visualizations</h2>
                <p>Interactive visualizations are available in the following HTML files:</p>
                <ul>
                    <li><strong>cost_by_disease.html</strong> - Average treatment cost comparison by disease</li>
                    <li><strong>total_cost_by_disease.html</strong> - Total treatment cost burden by disease</li>
                    <li><strong>disease_distribution.html</strong> - Patient distribution across diseases</li>
                    <li><strong>hospital_stay_analysis.html</strong> - Hospital stay patterns by disease</li>
                    <li><strong>cost_efficiency.html</strong> - Cost efficiency metrics (cost per hospital day)</li>
                    <li><strong>age_cost_scatter.html</strong> - Relationship between patient age and treatment cost</li>
                    <li><strong>correlation_heatmap.html</strong> - Correlation analysis between key variables</li>
                </ul>
                
                <div class="footer">
                    <p><strong>Report Prepared:</strong> {self.report_date}</p>
                    <p>This analysis is provided for healthcare business analyst and health economics decision-making. All figures are based on the provided patient dataset.</p>
                    <p><em>Confidential: For Internal Use Only</em></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _build_text_report(self) -> str:
        """Build text report content.
        
        Returns:
            Text string for the report
        """
        summary = self.analysis_results['summary_statistics']
        disease_stats = self.analysis_results['disease_statistics']
        top_diseases = self.analysis_results['top_diseases']
        age_analysis = self.analysis_results['age_analysis']
        
        text = f"""
{'='*80}
HEALTHCARE COST AND DISEASE ANALYSIS - EXECUTIVE SUMMARY REPORT
{'='*80}

Report Generated: {self.report_date}
Total Patients Analyzed: {int(summary['Total Patients'])}
Total Unique Diseases: {int(summary['Total Unique Diseases'])}

{'-'*80}
KEY PERFORMANCE INDICATORS
{'-'*80}

Total Treatment Cost:           ${summary['Total Treatment Cost']:>15,.0f}
Average Treatment Cost:         ${summary['Average Treatment Cost']:>15,.0f}
Median Treatment Cost:          ${summary['Median Treatment Cost']:>15,.0f}
Minimum Treatment Cost:         ${summary['Min Treatment Cost']:>15,.0f}
Maximum Treatment Cost:         ${summary['Max Treatment Cost']:>15,.0f}
Average Hospital Stay:          {summary['Average Hospital Stay (days)']:>15.1f} days
Average Patient Age:            {summary['Average Patient Age']:>15.1f} years

{'-'*80}
KEY FINDINGS
{'-'*80}

1. MOST EXPENSIVE DISEASE
   Disease: {top_diseases.index[0]}
   Average Cost: ${top_diseases.iloc[0]['Average Cost']:,.0f}
   Patient Count: {int(top_diseases.iloc[0]['Patient Count'])}
   Total Cost: ${top_diseases.iloc[0]['Total Cost']:,.0f}

2. LEAST EXPENSIVE DISEASE
   Disease: {top_diseases.index[-1]}
   Average Cost: ${top_diseases.iloc[-1]['Average Cost']:,.0f}
   Patient Count: {int(top_diseases.iloc[-1]['Patient Count'])}
   Total Cost: ${top_diseases.iloc[-1]['Total Cost']:,.0f}

{'-'*80}
COST ANALYSIS BY DISEASE
{'-'*80}

{'Disease':<20} {'Patients':>10} {'Avg Cost':>15} {'Total Cost':>15} {'Avg Days':>10}
{'-'*70}
"""
        
        for disease in disease_stats.index:
            row = disease_stats.loc[disease]
            text += f"{disease:<20} {int(row['Patient Count']):>10} ${row['Average Cost']:>14,.0f} ${row['Total Cost']:>14,.0f} {row['Avg Hospital Days']:>10.1f}\n"
        
        text += f"""
{'-'*80}
AGE-BASED COST ANALYSIS
{'-'*80}

{'Age Group':<15} {'Patients':>10} {'Avg Cost':>15} {'Total Cost':>15} {'Avg Days':>10}
{'-'*65}
"""
        
        for age_group in age_analysis.index:
            row = age_analysis.loc[age_group]
            text += f"{str(age_group):<15} {int(row['Patient Count']):>10} ${row['Average Cost']:>14,.0f} ${row['Total Cost']:>14,.0f} {row['Avg Hospital Days']:>10.1f}\n"
        
        text += f"""
{'-'*80}
RECOMMENDATIONS
{'-'*80}

1. RESOURCE ALLOCATION
   - Prioritize high-cost, high-volume diseases for maximum ROI
   - Allocate budget proportionally to disease burden
   - Monitor cost trends for strategic planning

2. TREATMENT OPTIMIZATION
   - Review treatment protocols for high-cost diseases
   - Identify best practices from cost-efficient disease management
   - Implement process improvements for cost reduction

3. PREVENTIVE CARE STRATEGIES
   - Emphasize prevention in high-risk age groups
   - Develop targeted intervention programs
   - Monitor outcomes and cost-effectiveness

4. HOSPITAL STAY REDUCTION
   - Target diseases with longest average stays
   - Implement care pathway optimization
   - Consider outpatient and remote monitoring options

{'-'*80}
VISUALIZATIONS AVAILABLE
{'-'*80}

- cost_by_disease.html: Average treatment cost comparison
- total_cost_by_disease.html: Total cost burden analysis
- disease_distribution.html: Patient distribution patterns
- hospital_stay_analysis.html: Length of stay analysis
- cost_efficiency.html: Cost per hospital day metrics
- age_cost_scatter.html: Age vs cost relationships
- correlation_heatmap.html: Variable correlation analysis

{'-'*80}
Confidential - For Internal Use Only
Report prepared for healthcare business analyst and health economics applications
{'='*80}
        """
        
        return text

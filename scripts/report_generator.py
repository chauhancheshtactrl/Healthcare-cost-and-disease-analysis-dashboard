"""
Executive Summary Report Generator
Creates professional reports for healthcare analysis
"""

import pandas as pd
from datetime import datetime
from typing import Dict, Any


class ExecutiveSummaryReport:
    """Generate professional executive summary reports"""
    
    def __init__(self, df: pd.DataFrame, analyzer_obj=None):
        """
        Initialize report generator
        
        Parameters:
        -----------
        df : pd.DataFrame
            Healthcare dataset
        analyzer_obj : HealthcareCostAnalyzer, optional
            Pre-initialized analyzer object
        """
        self.df = df
        self.analyzer = analyzer_obj
    
    def generate_report(self, output_file: str = 'reports/executive_summary.txt') -> str:
        """
        Generate comprehensive executive summary report
        
        Parameters:
        -----------
        output_file : str
            Path to save the report
            
        Returns:
        --------
        str
            Report content
        """
        
        report_content = self._build_report()
        
        # Save to file
        with open(output_file, 'w') as f:
            f.write(report_content)
        
        print(f"✅ Report saved to: {output_file}")
        return report_content
    
    def _build_report(self) -> str:
        """Build the complete report content"""
        
        report = []
        report.append("=" * 80)
        report.append("HEALTHCARE COST AND DISEASE ANALYSIS")
        report.append("EXECUTIVE SUMMARY REPORT")
        report.append("=" * 80)
        report.append("")
        report.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # 1. EXECUTIVE SUMMARY
        report.extend(self._section_executive_summary())
        
        # 2. KEY FINDINGS
        report.extend(self._section_key_findings())
        
        # 3. COST ANALYSIS
        report.extend(self._section_cost_analysis())
        
        # 4. DISEASE BURDEN
        report.extend(self._section_disease_burden())
        
        # 5. PATIENT DEMOGRAPHICS
        report.extend(self._section_demographics())
        
        # 6. OPERATIONAL METRICS
        report.extend(self._section_operational_metrics())
        
        # 7. RECOMMENDATIONS
        report.extend(self._section_recommendations())
        
        # 8. CONCLUSION
        report.extend(self._section_conclusion())
        
        return "\n".join(report)
    
    def _section_executive_summary(self) -> list:
        """Generate executive summary section"""
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("1. EXECUTIVE SUMMARY")
        lines.append("=" * 80)
        lines.append("")
        
        total_patients = len(self.df)
        total_diseases = self.df['Disease'].nunique()
        total_expenditure = self.df['Treatment Cost'].sum()
        avg_cost = self.df['Treatment Cost'].mean()
        
        lines.append(f"This comprehensive analysis examines healthcare expenditure patterns and disease")
        lines.append(f"burden across {total_patients:,} patient records covering {total_diseases} distinct diseases.")
        lines.append("")
        lines.append(f"Total Healthcare Expenditure:    ${total_expenditure:,.2f}")
        lines.append(f"Average Cost per Patient:        ${avg_cost:,.2f}")
        lines.append(f"Total Patients Analyzed:         {total_patients:,}")
        lines.append(f"Number of Diseases:              {total_diseases}")
        lines.append("")
        
        return lines
    
    def _section_key_findings(self) -> list:
        """Generate key findings section"""
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("2. KEY FINDINGS")
        lines.append("=" * 80)
        lines.append("")
        
        # Most expensive diseases
        most_expensive_avg = self.df.groupby('Disease')['Treatment Cost'].mean().sort_values(ascending=False).head(1)
        most_expensive_total = self.df.groupby('Disease')['Treatment Cost'].sum().sort_values(ascending=False).head(1)
        most prevalent = self.df['Disease'].value_counts().head(1)
        
        lines.append("KEY OBSERVATIONS:")
        lines.append("")
        lines.append(f"• Most Expensive Disease (by avg cost):")
        lines.append(f"  {most_expensive_avg.index[0]}: ${most_expensive_avg.values[0]:,.2f} per patient")
        lines.append("")
        lines.append(f"• Highest Total Expenditure:")
        lines.append(f"  {most_expensive_total.index[0]}: ${most_expensive_total.values[0]:,.2f}")
        lines.append("")
        lines.append(f"• Most Prevalent Disease:")
        lines.append(f"  {most_prevalent.index[0]}: {most_prevalent.values[0]:,} patients ({most_prevalent.values[0]/len(self.df)*100:.1f}%)")
        lines.append("")
        lines.append(f"• Average Hospital Stay: {self.df['Hospital Stay Days'].mean():.1f} days")
        lines.append(f"• Cost-Stay Correlation: {self.df['Hospital Stay Days'].corr(self.df['Treatment Cost']):.3f}")
        lines.append("")
        
        return lines
    
    def _section_cost_analysis(self) -> list:
        """Generate cost analysis section"""
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("3. COST ANALYSIS")
        lines.append("=" * 80)
        lines.append("")
        
        lines.append("3.1 OVERALL COST STATISTICS")
        lines.append("-" * 40)
        
        cost_stats = {
            'Total Expenditure': self.df['Treatment Cost'].sum(),
            'Average Cost': self.df['Treatment Cost'].mean(),
            'Median Cost': self.df['Treatment Cost'].median(),
            'Minimum Cost': self.df['Treatment Cost'].min(),
            'Maximum Cost': self.df['Treatment Cost'].max(),
            'Standard Deviation': self.df['Treatment Cost'].std()
        }
        
        for metric, value in cost_stats.items():
            lines.append(f"{metric:<25} ${value:>12,.2f}")
        
        lines.append("")
        lines.append("3.2 COST DISTRIBUTION BY DISEASE")
        lines.append("-" * 40)
        lines.append("")
        
        cost_by_disease = self.df.groupby('Disease').agg({
            'Treatment Cost': ['sum', 'mean', 'count']
        }).round(2)
        cost_by_disease.columns = ['Total', 'Average', 'Count']
        cost_by_disease = cost_by_disease.sort_values('Total', ascending=False)
        
        lines.append(f"{'Disease':<20} {'Total Cost':>15} {'Avg Cost':>15} {'Patients':>10} {'% of Total':>10}")
        lines.append("-" * 80)
        
        total_cost = cost_by_disease['Total'].sum()
        for disease, row in cost_by_disease.iterrows():
            pct = (row['Total'] / total_cost) * 100
            lines.append(f"{disease:<20} ${row['Total']:>14,.0f} ${row['Average']:>14,.0f} {row['Count']:>10.0f} {pct:>9.1f}%")
        
        lines.append("")
        
        return lines
    
    def _section_disease_burden(self) -> list:
        """Generate disease burden section"""
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("4. DISEASE BURDEN ANALYSIS")
        lines.append("=" * 80)
        lines.append("")
        
        disease_stats = self.df.groupby('Disease').agg({
            'Patient ID': 'count',
            'Treatment Cost': 'mean',
            'Hospital Stay Days': 'mean'
        }).round(2)
        disease_stats.columns = ['Patient Count', 'Avg Cost', 'Avg Stay Days']
        disease_stats['% of Patients'] = (disease_stats['Patient Count'] / disease_stats['Patient Count'].sum() * 100).round(1)
        disease_stats = disease_stats.sort_values('Patient Count', ascending=False)
        
        lines.append(f"{'Disease':<20} {'Patients':>10} {'% of Total':>12} {'Avg Cost':>15} {'Avg Stay':>12}")
        lines.append("-" * 80)
        
        for disease, row in disease_stats.iterrows():
            lines.append(f"{disease:<20} {row['Patient Count']:>10.0f} {row['% of Patients']:>11.1f}% ${row['Avg Cost']:>14,.0f} {row['Avg Stay Days']:>11.1f}d")
        
        lines.append("")
        
        return lines
    
    def _section_demographics(self) -> list:
        """Generate patient demographics section"""
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("5. PATIENT DEMOGRAPHICS")
        lines.append("=" * 80)
        lines.append("")
        
        lines.append("AGE STATISTICS")
        lines.append("-" * 40)
        lines.append(f"Average Age:           {self.df['Age'].mean():>6.1f} years")
        lines.append(f"Median Age:            {self.df['Age'].median():>6.1f} years")
        lines.append(f"Age Range:             {self.df['Age'].min():.0f} - {self.df['Age'].max():.0f} years")
        lines.append(f"Standard Deviation:    {self.df['Age'].std():>6.1f} years")
        lines.append("")
        
        lines.append("AGE GROUP DISTRIBUTION")
        lines.append("-" * 40)
        
        age_bins = [0, 30, 40, 50, 60, 70, 100]
        age_labels = ['18-30', '31-40', '41-50', '51-60', '61-70', '70+']
        df_temp = self.df.copy()
        df_temp['Age Group'] = pd.cut(df_temp['Age'], bins=age_bins, labels=age_labels)
        
        age_dist = df_temp.groupby('Age Group', observed=True).agg({
            'Patient ID': 'count',
            'Treatment Cost': 'mean',
            'Hospital Stay Days': 'mean'
        }).round(2)
        age_dist.columns = ['Count', 'Avg Cost', 'Avg Stay']
        
        lines.append(f"{'Age Group':<12} {'Patients':>10} {'% of Total':>12} {'Avg Cost':>15} {'Avg Stay':>12}")
        lines.append("-" * 70)
        
        total = age_dist['Count'].sum()
        for age_group, row in age_dist.iterrows():
            pct = (row['Count'] / total) * 100
            lines.append(f"{age_group:<12} {row['Count']:>10.0f} {pct:>11.1f}% ${row['Avg Cost']:>14,.0f} {row['Avg Stay']:>11.1f}d")
        
        lines.append("")
        
        return lines
    
    def _section_operational_metrics(self) -> list:
        """Generate operational metrics section"""
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("6. OPERATIONAL METRICS")
        lines.append("=" * 80)
        lines.append("")
        
        lines.append("HOSPITAL STAY ANALYSIS")
        lines.append("-" * 40)
        
        stay_stats = {
            'Average Hospital Stay': self.df['Hospital Stay Days'].mean(),
            'Median Hospital Stay': self.df['Hospital Stay Days'].median(),
            'Minimum Stay': self.df['Hospital Stay Days'].min(),
            'Maximum Stay': self.df['Hospital Stay Days'].max(),
            'Standard Deviation': self.df['Hospital Stay Days'].std()
        }
        
        for metric, value in stay_stats.items():
            lines.append(f"{metric:<30} {value:>8.1f} days")
        
        lines.append("")
        lines.append("COST EFFICIENCY METRICS")
        lines.append("-" * 40)
        
        efficiency = self.df.groupby('Disease').agg({
            'Treatment Cost': 'mean',
            'Hospital Stay Days': 'mean'
        })
        efficiency['Cost per Day'] = (efficiency['Treatment Cost'] / efficiency['Hospital Stay Days']).round(2)
        efficiency = efficiency.sort_values('Cost per Day', ascending=False)
        
        lines.append(f"{'Disease':<20} {'Cost per Day':>15}")
        lines.append("-" * 40)
        
        for disease, row in efficiency.iterrows():
            lines.append(f"{disease:<20} ${row['Cost per Day']:>14,.2f}")
        
        lines.append("")
        
        return lines
    
    def _section_recommendations(self) -> list:
        """Generate recommendations section"""
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("7. RECOMMENDATIONS")
        lines.append("=" * 80)
        lines.append("")
        
        most_expensive = self.df.groupby('Disease')['Treatment Cost'].mean().idxmax()
        highest_prevalence = self.df['Disease'].value_counts().index[0]
        avg_stay = self.df['Hospital Stay Days'].mean()
        
        lines.append("Based on the analysis, the following recommendations are proposed:")
        lines.append("")
        lines.append(f"1. COST MANAGEMENT")
        lines.append(f"   • Focus on {most_expensive} management, the most expensive disease")
        lines.append(f"   • Implement evidence-based clinical pathways to reduce treatment costs")
        lines.append(f"   • Review outlier cases for potential cost optimization opportunities")
        lines.append("")
        lines.append(f"2. DISEASE PREVENTION")
        lines.append(f"   • Prioritize {highest_prevalence} prevention and early intervention")
        lines.append(f"   • Develop targeted screening and education programs")
        lines.append("")
        lines.append(f"3. OPERATIONAL EFFICIENCY")
        lines.append(f"   • Evaluate hospital stay patterns (average: {avg_stay:.1f} days)")
        lines.append(f"   • Implement care coordination to reduce length of stay")
        lines.append(f"   • Enhance discharge planning and follow-up care")
        lines.append("")
        lines.append("4. DATA-DRIVEN DECISION MAKING")
        lines.append("   • Establish regular monitoring of these key metrics")
        lines.append("   • Create dashboards for real-time cost tracking")
        lines.append("   • Benchmark against industry standards")
        lines.append("")
        
        return lines
    
    def _section_conclusion(self) -> list:
        """Generate conclusion section"""
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("8. CONCLUSION")
        lines.append("=" * 80)
        lines.append("")
        
        lines.append("This analysis provides valuable insights into healthcare expenditure patterns and")
        lines.append("disease burden. The identified trends and metrics can guide strategic decision-making")
        lines.append("to optimize healthcare delivery and resource allocation.")
        lines.append("")
        lines.append("Key priorities should focus on high-cost diseases, prevalent conditions, and")
        lines.append("operational efficiency improvements to maximize patient outcomes while controlling costs.")
        lines.append("")
        lines.append("=" * 80)
        lines.append(f"End of Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)
        
        return lines


def generate_html_report(df: pd.DataFrame, output_file: str = 'reports/executive_summary.html') -> str:
    """
    Generate HTML version of the report
    
    Parameters:
    -----------
    df : pd.DataFrame
        Healthcare dataset
    output_file : str
        Path to save the HTML report
        
    Returns:
    --------
    str
        HTML content
    """
    
    total_patients = len(df)
    total_diseases = df['Disease'].nunique()
    total_expenditure = df['Treatment Cost'].sum()
    avg_cost = df['Treatment Cost'].mean()
    
    cost_by_disease = df.groupby('Disease')['Treatment Cost'].agg(['sum', 'mean', 'count']).sort_values('sum', ascending=False)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Healthcare Cost and Disease Analysis - Executive Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #1a5490;
                text-align: center;
                border-bottom: 3px solid #1a5490;
                padding-bottom: 15px;
            }}
            h2 {{
                color: #2a7db8;
                margin-top: 30px;
                border-left: 5px solid #2a7db8;
                padding-left: 15px;
            }}
            .metric {{
                display: inline-block;
                width: 22%;
                margin: 2%;
                padding: 20px;
                background-color: #f0f8ff;
                border-radius: 5px;
                text-align: center;
                border-left: 4px solid #1a5490;
            }}
            .metric-value {{
                font-size: 24px;
                font-weight: bold;
                color: #1a5490;
            }}
            .metric-label {{
                font-size: 12px;
                color: #666;
                margin-top: 5px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th {{
                background-color: #1a5490;
                color: white;
                padding: 12px;
                text-align: left;
            }}
            td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                color: #999;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Healthcare Cost and Disease Analysis</h1>
            <h2>Executive Summary Report</h2>
            <p>Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            
            <h2>Key Metrics</h2>
            <div class="metric">
                <div class="metric-value">{total_patients:,}</div>
                <div class="metric-label">Total Patients</div>
            </div>
            <div class="metric">
                <div class="metric-value">{total_diseases}</div>
                <div class="metric-label">Diseases</div>
            </div>
            <div class="metric">
                <div class="metric-value">${total_expenditure/1e6:.1f}M</div>
                <div class="metric-label">Total Expenditure</div>
            </div>
            <div class="metric">
                <div class="metric-value">${avg_cost:,.0f}</div>
                <div class="metric-label">Avg Cost/Patient</div>
            </div>
            
            <h2>Cost by Disease</h2>
            <table>
                <thead>
                    <tr>
                        <th>Disease</th>
                        <th>Total Cost</th>
                        <th>Average Cost</th>
                        <th>Patient Count</th>
                        <th>% of Total</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    total_cost = cost_by_disease['sum'].sum()
    for disease, row in cost_by_disease.iterrows():
        pct = (row['sum'] / total_cost) * 100
        html_content += f"""
                    <tr>
                        <td>{disease}</td>
                        <td>${row['sum']:,.0f}</td>
                        <td>${row['mean']:,.0f}</td>
                        <td>{int(row['count'])}</td>
                        <td>{pct:.1f}%</td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
            
            <div class="footer">
                <p>This report is based on analysis of healthcare expenditure and disease burden data.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"✅ HTML report saved to: {output_file}")
    return html_content


if __name__ == "__main__":
    from data.generate_sample_data import generate_healthcare_data
    
    # Generate sample data
    df = generate_healthcare_data(n_records=1000)
    
    # Generate text report
    report_gen = ExecutiveSummaryReport(df)
    report_content = report_gen.generate_report('reports/executive_summary.txt')
    print(report_content)
    
    # Generate HTML report
    generate_html_report(df, 'reports/executive_summary.html')

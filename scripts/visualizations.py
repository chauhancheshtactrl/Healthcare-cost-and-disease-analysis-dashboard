"""
Healthcare Visualizations Module
Creates comprehensive charts and dashboards for healthcare analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional


class HealthcareVisualizer:
    """Create visualizations for healthcare cost and disease analysis"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize visualizer with healthcare dataset
        
        Parameters:
        -----------
        df : pd.DataFrame
            Healthcare dataset
        """
        self.df = df.copy()
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (14, 8)
        plt.rcParams['font.size'] = 10
    
    # ==================== INDIVIDUAL CHARTS ====================
    
    def plot_cost_by_disease(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create bar chart of total costs by disease
        
        Parameters:
        -----------
        save_path : str, optional
            Path to save the figure
            
        Returns:
        --------
        plt.Figure
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        cost_by_disease = self.df.groupby('Disease')['Treatment Cost'].sum().sort_values(ascending=False)
        
        colors = sns.color_palette("husl", len(cost_by_disease))
        bars = ax.bar(range(len(cost_by_disease)), cost_by_disease.values, color=colors)
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, cost_by_disease.values)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50000,
                   f'${value/1e6:.1f}M', ha='center', va='bottom', fontweight='bold')
        
        ax.set_xlabel('Disease', fontsize=12, fontweight='bold')
        ax.set_ylabel('Total Treatment Cost ($)', fontsize=12, fontweight='bold')
        ax.set_title('Total Healthcare Expenditure by Disease', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticklabels(cost_by_disease.index, rotation=45, ha='right')
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.0f}M'))
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {save_path}")
        
        return fig
    
    def plot_average_cost_by_disease(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create bar chart of average costs by disease
        
        Parameters:
        -----------
        save_path : str, optional
            Path to save the figure
            
        Returns:
        --------
        plt.Figure
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        avg_cost = self.df.groupby('Disease')['Treatment Cost'].mean().sort_values(ascending=False)
        
        colors = sns.color_palette("coolwarm", len(avg_cost))
        bars = ax.barh(range(len(avg_cost)), avg_cost.values, color=colors)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, avg_cost.values)):
            ax.text(value + 500, bar.get_y() + bar.get_height()/2,
                   f'${value:,.0f}', ha='left', va='center', fontweight='bold')
        
        ax.set_yticks(range(len(avg_cost)))
        ax.set_yticklabels(avg_cost.index)
        ax.set_xlabel('Average Treatment Cost ($)', fontsize=12, fontweight='bold')
        ax.set_title('Average Treatment Cost by Disease', fontsize=14, fontweight='bold', pad=20)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K'))
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {save_path}")
        
        return fig
    
    def plot_disease_prevalence(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create pie chart of disease prevalence
        
        Parameters:
        -----------
        save_path : str, optional
            Path to save the figure
            
        Returns:
        --------
        plt.Figure
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        disease_counts = self.df['Disease'].value_counts()
        colors = sns.color_palette("Set3", len(disease_counts))
        
        wedges, texts, autotexts = ax.pie(disease_counts.values, 
                                           labels=disease_counts.index,
                                           autopct='%1.1f%%',
                                           colors=colors,
                                           startangle=90)
        
        # Enhance text
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        ax.set_title('Disease Prevalence Distribution', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {save_path}")
        
        return fig
    
    def plot_cost_vs_stay(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create scatter plot of treatment cost vs hospital stay days
        
        Parameters:
        -----------
        save_path : str, optional
            Path to save the figure
            
        Returns:
        --------
        plt.Figure
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Create scatter plot with disease coloring
        diseases = self.df['Disease'].unique()
        colors = sns.color_palette("husl", len(diseases))
        
        for disease, color in zip(diseases, colors):
            mask = self.df['Disease'] == disease
            ax.scatter(self.df[mask]['Hospital Stay Days'], 
                      self.df[mask]['Treatment Cost'],
                      label=disease, alpha=0.6, s=50, color=color)
        
        # Add trend line
        z = np.polyfit(self.df['Hospital Stay Days'], self.df['Treatment Cost'], 1)
        p = np.poly1d(z)
        ax.plot(self.df['Hospital Stay Days'].sort_values(), 
               p(self.df['Hospital Stay Days'].sort_values()),
               "r--", alpha=0.8, linewidth=2, label='Trend')
        
        correlation = self.df['Hospital Stay Days'].corr(self.df['Treatment Cost'])
        
        ax.set_xlabel('Hospital Stay Days', fontsize=12, fontweight='bold')
        ax.set_ylabel('Treatment Cost ($)', fontsize=12, fontweight='bold')
        ax.set_title(f'Treatment Cost vs Hospital Stay Duration (Correlation: {correlation:.2f})', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper left', fontsize=9)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K'))
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {save_path}")
        
        return fig
    
    def plot_cost_by_age_group(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create box plot of costs by age group
        
        Parameters:
        -----------
        save_path : str, optional
            Path to save the figure
            
        Returns:
        --------
        plt.Figure
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create age groups
        age_bins = [0, 30, 40, 50, 60, 70, 100]
        age_labels = ['18-30', '31-40', '41-50', '51-60', '61-70', '70+']
        df_temp = self.df.copy()
        df_temp['Age Group'] = pd.cut(df_temp['Age'], bins=age_bins, labels=age_labels)
        
        sns.boxplot(data=df_temp, x='Age Group', y='Treatment Cost', ax=ax, palette='Set2')
        
        ax.set_xlabel('Age Group', fontsize=12, fontweight='bold')
        ax.set_ylabel('Treatment Cost ($)', fontsize=12, fontweight='bold')
        ax.set_title('Treatment Cost Distribution by Age Group', fontsize=14, fontweight='bold', pad=20)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K'))
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {save_path}")
        
        return fig
    
    def plot_disease_cost_heatmap(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create heatmap of disease statistics
        
        Parameters:
        -----------
        save_path : str, optional
            Path to save the figure
            
        Returns:
        --------
        plt.Figure
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create disease statistics matrix
        disease_stats = self.df.groupby('Disease').agg({
            'Treatment Cost': 'mean',
            'Hospital Stay Days': 'mean',
            'Age': 'mean',
            'Patient ID': 'count'
        }).round(0)
        
        # Normalize for heatmap
        disease_stats_norm = (disease_stats - disease_stats.min()) / (disease_stats.max() - disease_stats.min())
        disease_stats_norm.columns = ['Avg Cost', 'Avg Stay', 'Avg Age', 'Patient Count']
        
        sns.heatmap(disease_stats_norm.T, annot=disease_stats.T, fmt='.0f', 
                   cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Normalized Value'})
        
        ax.set_title('Disease Statistics Heatmap', fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Disease', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {save_path}")
        
        return fig
    
    # ==================== DASHBOARD ====================
    
    def create_executive_dashboard(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create comprehensive executive dashboard
        
        Parameters:
        -----------
        save_path : str, optional
            Path to save the figure
            
        Returns:
        --------
        plt.Figure
            Matplotlib figure object
        """
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Cost by Disease (Top)
        ax1 = fig.add_subplot(gs[0, :2])
        cost_by_disease = self.df.groupby('Disease')['Treatment Cost'].sum().sort_values(ascending=False)
        colors = sns.color_palette("husl", len(cost_by_disease))
        ax1.bar(range(len(cost_by_disease)), cost_by_disease.values, color=colors)
        ax1.set_xticklabels(cost_by_disease.index, rotation=45, ha='right')
        ax1.set_ylabel('Total Cost ($)', fontweight='bold')
        ax1.set_title('Total Healthcare Expenditure by Disease', fontweight='bold')
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
        ax1.grid(axis='y', alpha=0.3)
        
        # 2. Key Metrics (Top Right)
        ax2 = fig.add_subplot(gs[0, 2])
        ax2.axis('off')
        metrics_text = f"""
        KEY METRICS
        
        Total Patients: {len(self.df):,}
        Total Diseases: {self.df['Disease'].nunique()}
        Total Expenditure: ${self.df['Treatment Cost'].sum()/1e6:.1f}M
        Avg Cost/Patient: ${self.df['Treatment Cost'].mean():,.0f}
        Avg Stay: {self.df['Hospital Stay Days'].mean():.1f} days
        Avg Age: {self.df['Age'].mean():.1f} years
        """
        ax2.text(0.1, 0.5, metrics_text, fontsize=11, verticalalignment='center',
                fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # 3. Disease Prevalence (Middle Left)
        ax3 = fig.add_subplot(gs[1, 0])
        disease_counts = self.df['Disease'].value_counts().head(5)
        ax3.barh(range(len(disease_counts)), disease_counts.values, color=sns.color_palette("Set2", 5))
        ax3.set_yticks(range(len(disease_counts)))
        ax3.set_yticklabels(disease_counts.index)
        ax3.set_xlabel('Patient Count', fontweight='bold')
        ax3.set_title('Top 5 Diseases by Prevalence', fontweight='bold', fontsize=11)
        ax3.grid(axis='x', alpha=0.3)
        
        # 4. Cost Distribution (Middle Center)
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.hist(self.df['Treatment Cost'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
        ax4.axvline(self.df['Treatment Cost'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
        ax4.axvline(self.df['Treatment Cost'].median(), color='green', linestyle='--', linewidth=2, label='Median')
        ax4.set_xlabel('Treatment Cost ($)', fontweight='bold')
        ax4.set_ylabel('Frequency', fontweight='bold')
        ax4.set_title('Cost Distribution', fontweight='bold', fontsize=11)
        ax4.legend(fontsize=9)
        ax4.grid(axis='y', alpha=0.3)
        ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K'))
        
        # 5. Cost vs Stay (Middle Right)
        ax5 = fig.add_subplot(gs[1, 2])
        ax5.scatter(self.df['Hospital Stay Days'], self.df['Treatment Cost'], alpha=0.5, s=30)
        z = np.polyfit(self.df['Hospital Stay Days'], self.df['Treatment Cost'], 1)
        p = np.poly1d(z)
        ax5.plot(self.df['Hospital Stay Days'].sort_values(), p(self.df['Hospital Stay Days'].sort_values()),
                "r--", linewidth=2)
        correlation = self.df['Hospital Stay Days'].corr(self.df['Treatment Cost'])
        ax5.set_xlabel('Hospital Stay Days', fontweight='bold')
        ax5.set_ylabel('Treatment Cost ($)', fontweight='bold')
        ax5.set_title(f'Cost vs Stay (r={correlation:.2f})', fontweight='bold', fontsize=11)
        ax5.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K'))
        ax5.grid(alpha=0.3)
        
        # 6. Age Distribution (Bottom Left)
        ax6 = fig.add_subplot(gs[2, 0])
        ax6.hist(self.df['Age'], bins=20, color='lightcoral', edgecolor='black', alpha=0.7)
        ax6.set_xlabel('Age (years)', fontweight='bold')
        ax6.set_ylabel('Frequency', fontweight='bold')
        ax6.set_title('Patient Age Distribution', fontweight='bold', fontsize=11)
        ax6.grid(axis='y', alpha=0.3)
        
        # 7. Average Cost by Age Group (Bottom Center)
        ax7 = fig.add_subplot(gs[2, 1])
        age_bins = [0, 30, 40, 50, 60, 70, 100]
        age_labels = ['18-30', '31-40', '41-50', '51-60', '61-70', '70+']
        df_temp = self.df.copy()
        df_temp['Age Group'] = pd.cut(df_temp['Age'], bins=age_bins, labels=age_labels)
        age_cost = df_temp.groupby('Age Group', observed=True)['Treatment Cost'].mean()
        ax7.bar(range(len(age_cost)), age_cost.values, color='lightgreen', edgecolor='black')
        ax7.set_xticks(range(len(age_cost)))
        ax7.set_xticklabels(age_cost.index, rotation=45, ha='right')
        ax7.set_ylabel('Average Cost ($)', fontweight='bold')
        ax7.set_title('Average Cost by Age Group', fontweight='bold', fontsize=11)
        ax7.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K'))
        ax7.grid(axis='y', alpha=0.3)
        
        # 8. Top 5 Most Expensive Diseases (Bottom Right)
        ax8 = fig.add_subplot(gs[2, 2])
        avg_cost = self.df.groupby('Disease')['Treatment Cost'].mean().sort_values(ascending=False).head(5)
        ax8.barh(range(len(avg_cost)), avg_cost.values, color=sns.color_palette("coolwarm", 5))
        ax8.set_yticks(range(len(avg_cost)))
        ax8.set_yticklabels(avg_cost.index)
        ax8.set_xlabel('Average Cost ($)', fontweight='bold')
        ax8.set_title('Top 5 Most Expensive Diseases', fontweight='bold', fontsize=11)
        ax8.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K'))
        ax8.grid(axis='x', alpha=0.3)
        
        fig.suptitle('Healthcare Cost and Disease Analysis - Executive Dashboard', 
                    fontsize=16, fontweight='bold', y=0.995)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {save_path}")
        
        return fig


if __name__ == "__main__":
    from data.generate_sample_data import generate_healthcare_data
    
    # Generate sample data
    df = generate_healthcare_data(n_records=1000)
    
    # Initialize visualizer
    viz = HealthcareVisualizer(df)
    
    # Create all visualizations
    print("Creating visualizations...")
    viz.plot_cost_by_disease('visualizations/01_cost_by_disease.png')
    viz.plot_average_cost_by_disease('visualizations/02_avg_cost_by_disease.png')
    viz.plot_disease_prevalence('visualizations/03_disease_prevalence.png')
    viz.plot_cost_vs_stay('visualizations/04_cost_vs_stay.png')
    viz.plot_cost_by_age_group('visualizations/05_cost_by_age_group.png')
    viz.plot_disease_cost_heatmap('visualizations/06_disease_heatmap.png')
    viz.create_executive_dashboard('visualizations/07_executive_dashboard.png')
    
    print("\n✅ All visualizations created successfully!")

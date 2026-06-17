"""
Visualization module for Healthcare Cost and Disease Analysis Dashboard
Generates various charts and graphs for data exploration and reporting
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class HealthcareVisualizer:
    """Class to handle all visualization tasks for healthcare data"""
    
    def __init__(self, style='seaborn', palette='husl', dpi=100):
        """Initialize visualizer with style settings"""
        sns.set_style(style)
        sns.set_palette(palette)
        self.dpi = dpi
        self.color_palette = sns.color_palette(palette)
        
    # ===================== STATIC/MATPLOTLIB CHARTS =====================
    
    def plot_cost_by_disease_bar(self, df, cost_col='Treatment Cost', disease_col='Disease', figsize=(14, 6)):
        """Bar chart showing average and total treatment cost by disease"""
        fig, axes = plt.subplots(1, 2, figsize=figsize, dpi=self.dpi)
        
        # Average cost by disease
        avg_cost = df.groupby(disease_col)[cost_col].mean().sort_values(ascending=False)
        axes[0].barh(avg_cost.index, avg_cost.values, color=self.color_palette)
        axes[0].set_xlabel('Average Treatment Cost ($)', fontsize=12, fontweight='bold')
        axes[0].set_title('Average Treatment Cost by Disease', fontsize=13, fontweight='bold')
        axes[0].grid(axis='x', alpha=0.3)
        
        # Total cost by disease
        total_cost = df.groupby(disease_col)[cost_col].sum().sort_values(ascending=False)
        axes[1].barh(total_cost.index, total_cost.values, color=self.color_palette)
        axes[1].set_xlabel('Total Treatment Cost ($)', fontsize=12, fontweight='bold')
        axes[1].set_title('Total Treatment Cost by Disease', fontsize=13, fontweight='bold')
        axes[1].grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_cost_distribution_boxplot(self, df, cost_col='Treatment Cost', disease_col='Disease', figsize=(14, 6)):
        """Box plot showing cost distribution by disease"""
        fig, ax = plt.subplots(figsize=figsize, dpi=self.dpi)
        
        sns.boxplot(data=df, x=disease_col, y=cost_col, palette=self.color_palette, ax=ax)
        ax.set_xlabel('Disease', fontsize=12, fontweight='bold')
        ax.set_ylabel('Treatment Cost ($)', fontsize=12, fontweight='bold')
        ax.set_title('Treatment Cost Distribution by Disease', fontsize=13, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_cost_pie_chart(self, df, cost_col='Treatment Cost', disease_col='Disease', figsize=(10, 8)):
        """Pie chart showing cost distribution across diseases"""
        fig, ax = plt.subplots(figsize=figsize, dpi=self.dpi)
        
        cost_by_disease = df.groupby(disease_col)[cost_col].sum().sort_values(ascending=False)
        colors = self.color_palette[:len(cost_by_disease)]
        
        wedges, texts, autotexts = ax.pie(cost_by_disease.values, labels=cost_by_disease.index, 
                                            autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title('Cost Distribution Across Diseases', fontsize=13, fontweight='bold', pad=20)
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        plt.tight_layout()
        return fig
    
    def plot_cost_vs_hospital_days_scatter(self, df, cost_col='Treatment Cost', 
                                           hospital_col='Hospital Stay Days', disease_col='Disease', figsize=(12, 7)):
        """Scatter plot showing relationship between hospital days and cost"""
        fig, ax = plt.subplots(figsize=figsize, dpi=self.dpi)
        
        diseases = df[disease_col].unique()
        colors = self.color_palette[:len(diseases)]
        
        for disease, color in zip(diseases, colors):
            mask = df[disease_col] == disease
            ax.scatter(df[mask][hospital_col], df[mask][cost_col], 
                      label=disease, alpha=0.6, s=100, color=color)
        
        ax.set_xlabel('Hospital Stay Days', fontsize=12, fontweight='bold')
        ax.set_ylabel('Treatment Cost ($)', fontsize=12, fontweight='bold')
        ax.set_title('Treatment Cost vs Hospital Stay Duration', fontsize=13, fontweight='bold')
        ax.legend(loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_hospital_days_by_disease(self, df, hospital_col='Hospital Stay Days', disease_col='Disease', figsize=(14, 6)):
        """Bar and violin plot for hospital stay duration by disease"""
        fig, axes = plt.subplots(1, 2, figsize=figsize, dpi=self.dpi)
        
        # Average hospital days
        avg_days = df.groupby(disease_col)[hospital_col].mean().sort_values(ascending=False)
        axes[0].barh(avg_days.index, avg_days.values, color=self.color_palette)
        axes[0].set_xlabel('Average Hospital Stay Days', fontsize=12, fontweight='bold')
        axes[0].set_title('Average Hospital Stay Duration by Disease', fontsize=13, fontweight='bold')
        axes[0].grid(axis='x', alpha=0.3)
        
        # Violin plot
        sns.violinplot(data=df, x=disease_col, y=hospital_col, palette=self.color_palette, ax=axes[1])
        axes[1].set_xlabel('Disease', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Hospital Stay Days', fontsize=12, fontweight='bold')
        axes[1].set_title('Hospital Stay Duration Distribution', fontsize=13, fontweight='bold')
        plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha='right')
        axes[1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_age_distribution_by_disease(self, df, age_col='Age', disease_col='Disease', figsize=(14, 6)):
        """Histograms showing age distribution by disease"""
        diseases = df[disease_col].unique()
        n_diseases = len(diseases)
        
        fig, axes = plt.subplots(1, 2, figsize=figsize, dpi=self.dpi)
        
        # Bar chart of average age
        avg_age = df.groupby(disease_col)[age_col].mean().sort_values(ascending=False)
        axes[0].barh(avg_age.index, avg_age.values, color=self.color_palette)
        axes[0].set_xlabel('Average Age (years)', fontsize=12, fontweight='bold')
        axes[0].set_title('Average Patient Age by Disease', fontsize=13, fontweight='bold')
        axes[0].grid(axis='x', alpha=0.3)
        
        # Distribution
        sns.boxplot(data=df, x=disease_col, y=age_col, palette=self.color_palette, ax=axes[1])
        axes[1].set_xlabel('Disease', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Age (years)', fontsize=12, fontweight='bold')
        axes[1].set_title('Patient Age Distribution by Disease', fontsize=13, fontweight='bold')
        plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha='right')
        axes[1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_heatmap_cost_by_age_disease(self, df, cost_col='Treatment Cost', age_col='Age', 
                                         disease_col='Disease', age_bins=5, figsize=(12, 6)):
        """Heatmap showing average cost by age groups and disease"""
        df_copy = df.copy()
        df_copy['Age Group'] = pd.cut(df_copy[age_col], bins=age_bins, labels=[f'Age {i}' for i in range(age_bins)])
        
        pivot_table = df_copy.pivot_table(values=cost_col, index='Age Group', 
                                          columns=disease_col, aggfunc='mean')
        
        fig, ax = plt.subplots(figsize=figsize, dpi=self.dpi)
        sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Avg Cost ($)'})
        ax.set_title('Average Treatment Cost: Age Groups vs Disease', fontsize=13, fontweight='bold')
        ax.set_xlabel('Disease', fontsize=12, fontweight='bold')
        ax.set_ylabel('Age Group', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def plot_cost_efficiency(self, df, cost_col='Treatment Cost', hospital_col='Hospital Stay Days', 
                            disease_col='Disease', figsize=(12, 6)):
        """Plot cost efficiency (cost per hospital day) by disease"""
        df_copy = df.copy()
        df_copy['Cost Per Day'] = df_copy[cost_col] / df_copy[hospital_col].replace(0, 1)
        
        fig, ax = plt.subplots(figsize=figsize, dpi=self.dpi)
        
        efficiency = df_copy.groupby(disease_col)['Cost Per Day'].mean().sort_values(ascending=False)
        bars = ax.barh(efficiency.index, efficiency.values, color=self.color_palette)
        
        ax.set_xlabel('Cost Per Hospital Day ($)', fontsize=12, fontweight='bold')
        ax.set_title('Treatment Cost Efficiency by Disease', fontsize=13, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, f'${width:.0f}', 
                   ha='left', va='center', fontweight='bold', fontsize=10)
        
        plt.tight_layout()
        return fig
    
    # ===================== INTERACTIVE PLOTLY CHARTS =====================
    
    def create_interactive_dashboard(self, df, cost_col='Treatment Cost', disease_col='Disease',
                                    hospital_col='Hospital Stay Days', age_col='Age'):
        """Create an interactive Plotly dashboard with multiple subplots"""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Average Cost by Disease', 'Cost Distribution', 
                          'Hospital Days vs Cost', 'Patient Age by Disease'),
            specs=[[{'type': 'bar'}, {'type': 'pie'}],
                   [{'type': 'scatter'}, {'type': 'box'}]]
        )
        
        # 1. Bar chart - Average cost by disease
        avg_cost = df.groupby(disease_col)[cost_col].mean().sort_values(ascending=False)
        fig.add_trace(
            go.Bar(x=avg_cost.index, y=avg_cost.values, name='Avg Cost', 
                   marker_color='indianred'),
            row=1, col=1
        )
        
        # 2. Pie chart - Cost distribution
        total_cost = df.groupby(disease_col)[cost_col].sum()
        fig.add_trace(
            go.Pie(labels=total_cost.index, values=total_cost.values, name='Cost Share'),
            row=1, col=2
        )
        
        # 3. Scatter plot - Cost vs Hospital Days
        for disease in df[disease_col].unique():
            mask = df[disease_col] == disease
            fig.add_trace(
                go.Scatter(x=df[mask][hospital_col], y=df[mask][cost_col], 
                          mode='markers', name=disease, 
                          marker=dict(size=8, opacity=0.6)),
                row=2, col=1
            )
        
        # 4. Box plot - Age by disease
        for disease in df[disease_col].unique():
            mask = df[disease_col] == disease
            fig.add_trace(
                go.Box(y=df[mask][age_col], name=disease, boxmean='sd'),
                row=2, col=2
            )
        
        # Update layout
        fig.update_xaxes(title_text='Disease', row=1, col=1)
        fig.update_yaxes(title_text='Average Cost ($)', row=1, col=1)
        fig.update_xaxes(title_text='Hospital Days', row=2, col=1)
        fig.update_yaxes(title_text='Treatment Cost ($)', row=2, col=1)
        fig.update_yaxes(title_text='Age (years)', row=2, col=2)
        
        fig.update_layout(height=900, showlegend=True, title_text="Healthcare Cost Analysis Dashboard",
                         hovermode='closest')
        
        return fig
    
    def create_interactive_cost_analysis(self, df, cost_col='Treatment Cost', disease_col='Disease'):
        """Create interactive cost analysis with dropdown filters"""
        
        cost_stats = df.groupby(disease_col)[cost_col].agg(['mean', 'sum', 'count', 'std']).reset_index()
        cost_stats.columns = ['Disease', 'Average', 'Total', 'Count', 'Std Dev']
        
        fig = px.bar(cost_stats, x='Disease', y=['Average', 'Total'], 
                    title='Treatment Cost Analysis by Disease',
                    labels={'value': 'Cost ($)', 'variable': 'Metric'},
                    barmode='group', template='plotly_white')
        
        fig.update_layout(hovermode='x unified', height=500)
        return fig
    
    def create_interactive_scatter_3d(self, df, cost_col='Treatment Cost', 
                                     hospital_col='Hospital Stay Days', age_col='Age', disease_col='Disease'):
        """Create 3D scatter plot: Cost vs Hospital Days vs Age"""
        
        fig = px.scatter_3d(df, x=hospital_col, y=cost_col, z=age_col, 
                           color=disease_col, size=cost_col, hover_data=[disease_col],
                           title='3D Analysis: Cost vs Hospital Days vs Patient Age',
                           labels={cost_col: 'Treatment Cost ($)', 
                                  hospital_col: 'Hospital Stay Days',
                                  age_col: 'Patient Age (years)'},
                           template='plotly_white')
        
        fig.update_layout(height=700)
        return fig
    
    # ===================== STATISTICAL CHARTS =====================
    
    def plot_statistical_summary(self, df, cost_col='Treatment Cost', disease_col='Disease', figsize=(14, 8)):
        """Create a summary statistics visualization"""
        fig, axes = plt.subplots(2, 2, figsize=figsize, dpi=self.dpi)
        
        # Distribution of costs
        axes[0, 0].hist(df[cost_col], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
        axes[0, 0].set_xlabel('Treatment Cost ($)', fontsize=11, fontweight='bold')
        axes[0, 0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
        axes[0, 0].set_title('Overall Cost Distribution', fontsize=12, fontweight='bold')
        axes[0, 0].grid(axis='y', alpha=0.3)
        
        # Q-Q plot for normality
        from scipy import stats
        stats.probplot(df[cost_col], dist="norm", plot=axes[0, 1])
        axes[0, 1].set_title('Q-Q Plot: Cost Normality Test', fontsize=12, fontweight='bold')
        axes[0, 1].grid(alpha=0.3)
        
        # Count of patients by disease
        disease_counts = df[disease_col].value_counts()
        axes[1, 0].bar(disease_counts.index, disease_counts.values, color=self.color_palette)
        axes[1, 0].set_xlabel('Disease', fontsize=11, fontweight='bold')
        axes[1, 0].set_ylabel('Number of Patients', fontsize=11, fontweight='bold')
        axes[1, 0].set_title('Patient Count by Disease', fontsize=12, fontweight='bold')
        plt.setp(axes[1, 0].xaxis.get_majorticklabels(), rotation=45, ha='right')
        axes[1, 0].grid(axis='y', alpha=0.3)
        
        # Summary statistics text
        axes[1, 1].axis('off')
        summary_text = f"""
        SUMMARY STATISTICS

        Total Patients: {len(df):,}
        Diseases: {df[disease_col].nunique()}
        
        Treatment Cost:
        • Mean: ${df[cost_col].mean():,.2f}
        • Median: ${df[cost_col].median():,.2f}
        • Std Dev: ${df[cost_col].std():,.2f}
        • Min: ${df[cost_col].min():,.2f}
        • Max: ${df[cost_col].max():,.2f}
        """
        axes[1, 1].text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
                       verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        return fig


def save_figures(figures_dict, output_path='reports/charts/'):
    """Save all figures to output path"""
    import os
    os.makedirs(output_path, exist_ok=True)
    
    for name, fig in figures_dict.items():
        if hasattr(fig, 'write_html'):  # Plotly figure
            fig.write_html(f"{output_path}{name}.html")
        else:  # Matplotlib figure
            fig.savefig(f"{output_path}{name}.png", dpi=300, bbox_inches='tight')
        print(f"Saved: {output_path}{name}")

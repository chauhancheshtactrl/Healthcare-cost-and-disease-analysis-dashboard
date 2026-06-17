"""Visualization module for healthcare data"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Tuple


class HealthcareVisualizer:
    """
    Creates professional visualizations for healthcare data analysis.
    """
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """Initialize visualizer.
        
        Args:
            style: Matplotlib style to use
        """
        self.style = style
        sns.set_palette("husl")
        
    def create_cost_by_disease_chart(self, analysis_df: pd.DataFrame) -> None:
        """Create bar chart of average treatment cost by disease.
        
        Args:
            analysis_df: DataFrame with disease cost analysis
        """
        fig = go.Figure()
        
        # Sort by average cost
        sorted_df = analysis_df.sort_values('Average Cost', ascending=True)
        
        fig.add_trace(go.Bar(
            y=sorted_df.index,
            x=sorted_df['Average Cost'],
            orientation='h',
            marker=dict(
                color=sorted_df['Average Cost'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Cost ($)")
            ),
            text=sorted_df['Average Cost'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Average Cost: $%{x:,.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Average Treatment Cost by Disease',
            xaxis_title='Average Cost ($)',
            yaxis_title='Disease',
            height=500,
            width=900,
            showlegend=False,
            hovermode='closest'
        )
        
        fig.write_html('reports/cost_by_disease.html')
        print("✓ Saved: cost_by_disease.html")
    
    def create_disease_distribution_chart(self, data: pd.DataFrame) -> None:
        """Create pie chart of disease distribution.
        
        Args:
            data: Original healthcare data
        """
        disease_counts = data['Disease'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=disease_counts.index,
            values=disease_counts.values,
            hovertemplate='<b>%{label}</b><br>Patients: %{value}<br>Percentage: %{percent}<extra></extra>',
            textposition='inside',
            textinfo='label+percent'
        )])
        
        fig.update_layout(
            title='Patient Distribution by Disease',
            height=600,
            width=900
        )
        
        fig.write_html('reports/disease_distribution.html')
        print("✓ Saved: disease_distribution.html")
    
    def create_total_cost_by_disease_chart(self, analysis_df: pd.DataFrame) -> None:
        """Create bar chart of total treatment cost by disease.
        
        Args:
            analysis_df: DataFrame with disease cost analysis
        """
        sorted_df = analysis_df.sort_values('Total Cost', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=sorted_df.index,
            x=sorted_df['Total Cost'],
            orientation='h',
            marker=dict(
                color=sorted_df['Total Cost'],
                colorscale='RdYlGn_r',
                showscale=True,
                colorbar=dict(title="Total Cost ($)")
            ),
            text=sorted_df['Total Cost'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Total Cost: $%{x:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Total Treatment Cost by Disease',
            xaxis_title='Total Cost ($)',
            yaxis_title='Disease',
            height=500,
            width=900,
            showlegend=False
        )
        
        fig.write_html('reports/total_cost_by_disease.html')
        print("✓ Saved: total_cost_by_disease.html")
    
    def create_hospital_stay_analysis(self, hospital_df: pd.DataFrame) -> None:
        """Create visualization of hospital stay patterns.
        
        Args:
            hospital_df: DataFrame with hospital stay analysis
        """
        sorted_df = hospital_df.sort_values('Avg Hospital Days', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=sorted_df.index,
            x=sorted_df['Avg Hospital Days'],
            orientation='h',
            marker=dict(
                color='#FF6B6B',
                opacity=0.8
            ),
            name='Avg Hospital Days',
            hovertemplate='<b>%{y}</b><br>Avg Hospital Days: %{x:.1f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Average Hospital Stay by Disease',
            xaxis_title='Days',
            yaxis_title='Disease',
            height=500,
            width=900,
            showlegend=False
        )
        
        fig.write_html('reports/hospital_stay_analysis.html')
        print("✓ Saved: hospital_stay_analysis.html")
    
    def create_cost_efficiency_chart(self, efficiency_df: pd.DataFrame) -> None:
        """Create cost efficiency visualization.
        
        Args:
            efficiency_df: DataFrame with cost efficiency metrics
        """
        sorted_df = efficiency_df.sort_values('Cost per Hospital Day', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=sorted_df.index,
            x=sorted_df['Cost per Hospital Day'],
            orientation='h',
            marker=dict(
                color=sorted_df['Cost per Hospital Day'],
                colorscale='Plasma',
                showscale=True,
                colorbar=dict(title="Cost per Day ($)")
            ),
            text=sorted_df['Cost per Hospital Day'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Cost per Hospital Day: $%{x:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Cost Efficiency: Treatment Cost per Hospital Day',
            xaxis_title='Cost per Hospital Day ($)',
            yaxis_title='Disease',
            height=500,
            width=900,
            showlegend=False
        )
        
        fig.write_html('reports/cost_efficiency.html')
        print("✓ Saved: cost_efficiency.html")
    
    def create_age_cost_scatter(self, data: pd.DataFrame) -> None:
        """Create scatter plot of age vs treatment cost.
        
        Args:
            data: Original healthcare data
        """
        fig = px.scatter(
            data,
            x='Age',
            y='Treatment Cost',
            color='Disease',
            size='Hospital Stay Days',
            hover_data=['Patient ID', 'Hospital Stay Days'],
            title='Treatment Cost vs Patient Age by Disease',
            labels={'Treatment Cost': 'Treatment Cost ($)', 'Age': 'Patient Age (years)'},
            height=600,
            width=900
        )
        
        fig.update_layout(
            hovermode='closest',
            template='plotly_white'
        )
        
        fig.write_html('reports/age_cost_scatter.html')
        print("✓ Saved: age_cost_scatter.html")
    
    def create_correlation_heatmap(self, correlation_df: pd.DataFrame) -> None:
        """Create correlation heatmap.
        
        Args:
            correlation_df: Correlation matrix
        """
        fig = go.Figure(data=go.Heatmap(
            z=correlation_df.values,
            x=correlation_df.columns,
            y=correlation_df.columns,
            colorscale='RdBu',
            zmid=0,
            text=correlation_df.values,
            texttemplate='%{text:.2f}',
            textfont={"size": 12},
            hovertemplate='%{y} vs %{x}: %{z:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Correlation Matrix: Healthcare Variables',
            height=500,
            width=600
        )
        
        fig.write_html('reports/correlation_heatmap.html')
        print("✓ Saved: correlation_heatmap.html")

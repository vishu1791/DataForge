import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Optional, Dict, Any
import os
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

class DataVisualizer:
    """Handles data visualization operations."""
    
    def __init__(self):
        try:
            plt.style.use('seaborn-v0_8')
        except OSError:
            try:
                plt.style.use('seaborn')
            except OSError:
                plt.style.use('default')
        except Exception:
            plt.style.use('default')
        
        # Set seaborn style
        try:
            sns.set_palette("husl")
        except Exception:
            pass
    
    @staticmethod
    def plot_distribution(
        df: pd.DataFrame, 
        column: str, 
        plot_type: str = 'histogram'
    ) -> go.Figure:
        """
        Create distribution plots for a column.
        
        Args:
            df: Input DataFrame
            column: Column name to plot
            plot_type: 'histogram', 'box', 'violin'
            
        Returns:
            Plotly figure object
        """
        if plot_type == 'histogram':
            fig = px.histogram(df, x=column, title=f'Distribution of {column}')
        elif plot_type == 'box':
            fig = px.box(df, y=column, title=f'Box Plot of {column}')
        elif plot_type == 'violin':
            fig = px.violin(df, y=column, title=f'Violin Plot of {column}')
        else:
            raise ValueError("plot_type must be 'histogram', 'box', or 'violin'")
        
        return fig
    
    @staticmethod
    def plot_correlation_matrix(df: pd.DataFrame) -> go.Figure:
        """Create correlation matrix heatmap."""
        numeric_df = df.select_dtypes(include=['number'])
        corr_matrix = numeric_df.corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix",
            color_continuous_scale="RdBu_r"
        )
        
        return fig
    
    @staticmethod
    def plot_scatter(
        df: pd.DataFrame, 
        x: str, 
        y: str, 
        color: Optional[str] = None
    ) -> go.Figure:
        """Create scatter plot."""
        fig = px.scatter(
            df, 
            x=x, 
            y=y, 
            color=color,
            title=f'Scatter Plot: {x} vs {y}'
        )
        
        return fig
    
    @staticmethod
    def plot_missing_values(df: pd.DataFrame) -> go.Figure:
        """Create missing values heatmap."""
        missing_data = df.isnull().sum()
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        
        if missing_data.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="No missing values found!",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20)
            )
        else:
            fig = px.bar(
                x=missing_data.index,
                y=missing_data.values,
                title="Missing Values Count by Column",
                labels={'x': 'Columns', 'y': 'Missing Values Count'}
            )
        
        return fig
    
    @staticmethod
    def plot_data_overview(df: pd.DataFrame) -> go.Figure:
        """Create data overview dashboard."""
        numeric_cols = df.select_dtypes(include=['number']).columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Data Types Distribution',
                'Missing Values Overview',
                'Numeric Columns Summary',
                'Dataset Shape'
            ),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "table"}, {"type": "indicator"}]]
        )
        
        # Data types pie chart
        dtype_counts = df.dtypes.value_counts()
        fig.add_trace(
            go.Pie(
                labels=dtype_counts.index,
                values=dtype_counts.values,
                name="Data Types"
            ),
            row=1, col=1
        )
        
        # Missing values bar chart
        missing_counts = df.isnull().sum()
        missing_counts = missing_counts[missing_counts > 0]
        if not missing_counts.empty:
            fig.add_trace(
                go.Bar(
                    x=missing_counts.index,
                    y=missing_counts.values,
                    name="Missing Values"
                ),
                row=1, col=2
            )
        
        # Numeric columns summary table
        if not numeric_cols.empty:
            summary_stats = df[numeric_cols].describe()
            # Convert summary stats to strings for table display
            header_values = ['Statistic'] + list(summary_stats.index)
            cell_values = [header_values]
            
            for col in summary_stats.columns:
                row_values = [col] + [f"{val:.2f}" if isinstance(val, (int, float)) else str(val) 
                               for val in summary_stats[col]]
                cell_values.append(row_values)
            
            fig.add_trace(
                go.Table(
                    header=dict(values=header_values, fill_color='lightblue'),
                    cells=dict(values=list(zip(*cell_values)), fill_color='lightgrey')
                ),
                row=2, col=1
            )
        
        # Dataset shape indicator
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=df.shape[0],
                title={"text": f"Rows × {df.shape[1]} Columns"},
                domain={'x': [0, 1], 'y': [0, 1]},
                number={'font': {'size': 40}},
                delta={'reference': df.shape[0] * 0.9}
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=False, title_text="Data Overview Dashboard")
        
        return fig
    
    @staticmethod
    def save_plot(fig: go.Figure, filename: str, output_dir: str = "outputs/plots") -> str:
        """
        Save plot to file.
        
        Args:
            fig: Plotly figure object
            filename: Output filename
            output_dir: Directory to save the plot
            
        Returns:
            Path to saved file
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        fig.write_html(filepath)
        
        return filepath

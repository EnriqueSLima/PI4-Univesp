import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
import pandas as pd

class ChartGenerator:
    @staticmethod
    def create_interactive_chart(df, x_col, y_col, chart_type='line'):
        """Cria gráficos interativos com Plotly"""
        if chart_type == 'line':
            fig = px.line(df, x=x_col, y=y_col, title=f'{y_col} por {x_col}')
        elif chart_type == 'bar':
            fig = px.bar(df, x=x_col, y=y_col, title=f'{y_col} por {x_col}')
        
        return plot(fig, output_type='div')
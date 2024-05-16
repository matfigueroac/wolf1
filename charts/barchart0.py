import pandas as pd
import plotly.graph_objects as go

def create_chart():
    # Data
    expected_hours = 1136
    logged_hours = 751.95

    # Create the bar chart using Plotly
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=['Expected Hours', 'Actual Logged Hours'],
        y=[expected_hours, logged_hours],
        text=[f'{expected_hours:.2f}', f'{logged_hours:.2f}'],
        textposition='outside',
        marker_color=['blue', 'red']
    ))

    # Customize layout
    fig.update_layout(
        title='Análisis Total Horas Registradas',
        xaxis_title='Categoría',
        yaxis_title='Horas',
        margin=dict(t=50, b=20, l=0, r=0)
    )

    return fig

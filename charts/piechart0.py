import pandas as pd
import plotly.express as px
import os

def create_chart():
    file_path = os.path.join(os.path.dirname(__file__), 'team_data G2_tipo de costo.csv')
    df = pd.read_csv(file_path, encoding='latin1')
    
    # Aggregate hours logged by cost type
    df_costos = df.groupby('Cost Type')['Hours Logged'].sum().reset_index()
    df_costos.columns = ['Tipo de Costo', 'Total Horas Registradas']
    
    # Calculate percentages
    total_horas = df_costos['Total Horas Registradas'].sum()
    df_costos['% Horas Totales'] = (df_costos['Total Horas Registradas'] / total_horas) * 100
    
    # Create pie chart using Plotly Express
    fig = px.pie(df_costos, values='Total Horas Registradas', names='Tipo de Costo',
                 title='Distribución de Horas Registradas por Tipo de Costo',
                 labels={'Total Horas Registradas':'Total Horas Registradas', 'Tipo de Costo':'Tipo de Costo'},
                 hole=0.3)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(margin=dict(t=50, b=20, l=0, r=0))

    return fig

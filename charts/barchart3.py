import pandas as pd
import plotly.graph_objects as go
import os

def create_chart():
    # Specify the path to your CSV file
    file_path = os.path.join(os.path.dirname(__file__), 'team_data G2_tipo de costo.csv')

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, encoding='latin1')

    # Convert the 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Check for the existence of the 'Cost Type' column
    if 'Cost Type' in df.columns:
        # Group logged hours by cost type
        df_costos = df.groupby('Cost Type')['Hours Logged'].sum().reset_index()
        df_costos.columns = ['Tipo de Costo', 'Total Horas Registradas']
        
        # Calculate the total hours logged
        total_horas = df_costos['Total Horas Registradas'].sum()
        
        # Calculate the percentage of each cost type
        df_costos['% Horas Totales'] = (df_costos['Total Horas Registradas'] / total_horas) * 100

        # Create the bar chart using Plotly
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df_costos['Tipo de Costo'],
            y=df_costos['Total Horas Registradas'],
            text=df_costos.apply(lambda row: f'{row["Total Horas Registradas"]:.1f} horas\n({row["% Horas Totales"]:.1f}%)', axis=1),
            textposition='auto',
            marker_color=['skyblue', 'orange']
        ))

        # Customize layout
        fig.update_layout(
            title='Total Horas Registradas por Tipo de Costo (Directo vs Indirecto)',
            xaxis_title='Tipo de Costo',
            yaxis_title='Total Horas Registradas',
            margin=dict(t=50, b=20, l=0, r=0)
        )

        return fig

    else:
        print("La columna 'Cost Type' no existe en el archivo CSV.")
        return go.Figure()

if __name__ == "__main__":
    fig = create_chart()
    fig.show()

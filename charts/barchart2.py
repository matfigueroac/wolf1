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

    # Extract the month and week number from the 'Date' column
    df['Mes'] = df['Date'].dt.strftime('%b')  # Month as abbreviated name
    df['Semana'] = df['Date'].dt.isocalendar().week

    # Define data for expected hours and weeks
    data = {
        'Mes': ['Jan', 'Jan', 'Jan', 'Jan', 'Feb', 'Feb', 'Feb', 'Feb', 'Mar', 'Mar', 'Mar', 'Mar', 'Apr', 'Apr', 'Apr', 'Apr'],
        'Semana': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        'Horas Esperadas Semanales': [120, 120, 120, 120, 80, 80, 80, 80, 80, 80, 80, 80, 20, 20, 20, 20],
        'Horas Registradas': [0] * 16  # Initially zero
    }

    # Create a DataFrame from the provided data
    df_expected = pd.DataFrame(data)

    # Group logged hours by month and week
    df_grouped = df.groupby(['Mes', 'Semana'])['Hours Logged'].sum().reset_index()

    # Combine both DataFrames
    df_combined = pd.merge(df_expected, df_grouped, on=['Mes', 'Semana'], how='left')
    df_combined['Horas Registradas'] = df_combined['Hours Logged'].fillna(0)  # Fill NA with zero
    df_combined.drop(columns=['Hours Logged'], inplace=True)  # Drop unnecessary column

    # Calculate percentage of logged hours relative to expected hours
    df_combined['%'] = (df_combined['Horas Registradas'] / df_combined['Horas Esperadas Semanales']) * 100

    # Define month order
    mes_order = ['Jan', 'Feb', 'Mar', 'Apr']
    df_combined['Mes'] = pd.Categorical(df_combined['Mes'], categories=mes_order, ordered=True)

    # Create label for x-axis in the format "Mes Semana X"
    df_combined['Mes_Semana'] = df_combined['Mes'].astype(str) + ' Semana ' + df_combined['Semana'].astype(str)

    # Create the bar chart using Plotly
    fig = go.Figure()

    # Expected hours bars (shifted left)
    fig.add_trace(go.Bar(
        x=df_combined['Mes_Semana'],
        y=df_combined['Horas Esperadas Semanales'],
        name='Horas Esperadas por Semana',
        marker_color='skyblue',
        opacity=0.7
    ))

    # Logged hours bars (shifted right)
    fig.add_trace(go.Bar(
        x=df_combined['Mes_Semana'],
        y=df_combined['Horas Registradas'],
        name='Horas Registradas',
        marker_color='orange',
        opacity=1.0
    ))

    # Customize layout
    fig.update_layout(
        title='Horas Registradas vs. Horas Esperadas por Semana (Enero - Abril) con Porcentaje de Cumplimiento',
        xaxis_title='Semana del Año',
        yaxis_title='Horas',
        barmode='group',
        legend_title='',
        margin=dict(t=50, b=20, l=0, r=0),
        bargap=0.15
    )

    # Add percentage on top of logged hours bars
    for i in range(len(df_combined)):
        fig.add_annotation(
            x=df_combined['Mes_Semana'][i],
            y=df_combined['Horas Registradas'][i] + 5,
            text=f'{df_combined["%"][i]:.1f}%',
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center"
        )

    return fig

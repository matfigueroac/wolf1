import pandas as pd
import plotly.graph_objects as go
import os

def create_chart():
    # Specify the path to your CSV file using a relative path
    file_path = os.path.join(os.path.dirname(__file__), 'team_data G2_tipo de costo.csv')

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, encoding='latin1')

    # Convert the 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Group logged hours by month
    df_monthly_logged = df.groupby(df['Date'].dt.strftime('%b'))['Hours Logged'].sum().reset_index()

    # Set the order of the months from January to April
    mes_order = ['Jan', 'Feb', 'Mar', 'Apr']
    df_monthly_logged['Date'] = pd.Categorical(df_monthly_logged['Date'], categories=mes_order, ordered=True)

    # Sort the DataFrame by the order of the months
    df_monthly_logged = df_monthly_logged.sort_values('Date').reset_index(drop=True)

    # Rename columns for clarity
    df_monthly_logged.columns = ['Mes', 'Horas Registradas']

    # Create the DataFrame of expected hours
    data = {
        'Mes': ['Jan', 'Feb', 'Mar', 'Apr'],
        'Horas Esperadas': [480, 320, 320, 80]  # Adjusted for April
    }

    df_expected = pd.DataFrame(data)

    # Combine both DataFrames
    df_combined = pd.merge(df_expected, df_monthly_logged, on='Mes')

    # Calculate the percentage of each bar
    df_combined['% Horas Registradas'] = (df_combined['Horas Registradas'] / df_combined['Horas Esperadas']) * 100

    # Create the bar chart using Plotly
    fig = go.Figure()

    # Expected hours bars (shifted left)
    fig.add_trace(go.Bar(
        x=df_combined['Mes'],
        y=df_combined['Horas Esperadas'],
        name='Horas Esperadas',
        marker_color='skyblue',
        opacity=0.7
    ))

    # Logged hours bars (shifted right)
    fig.add_trace(go.Bar(
        x=df_combined['Mes'],
        y=df_combined['Horas Registradas'],
        name='Horas Registradas Actualizadas',
        marker_color='orange',
        opacity=1.0
    ))

    # Add percentage on top of logged hours bars
    for i, row in df_combined.iterrows():
        fig.add_annotation(
            x=row['Mes'],
            y=row['Horas Registradas'] + 5,
            text=f'{row["% Horas Registradas"]:.1f}%',
            showarrow=False,
            font=dict(size=18, color="black"),
            align="center"
        )

    # Customize layout
    fig.update_layout(
        title='Comparación Actualizada de Horas Registradas vs. Horas Esperadas (Enero - Abril)',
        xaxis_title='Mes',
        yaxis_title='Horas',
        barmode='group',
        legend_title='',
        margin=dict(t=50, b=20, l=0, r=0),
        bargap=0.15
    )

    return fig

if __name__ == "__main__":
    fig = create_chart()
    fig.show()

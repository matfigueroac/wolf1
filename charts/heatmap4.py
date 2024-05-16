import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os

def create_heatmap4():
    # Especificar la ruta completa al archivo CSV
    file_path = os.path.join(os.path.dirname(__file__), 'team_data_Q2.csv')

    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv(file_path)

    # Calcular el nuevo Performance Ratio
    df['Performance Ratio'] = df['Hours Logged'] / df['Estimated Hours Logged']

    # Calcular los totales de Hours Logged y Estimated Hours Logged por cada ingeniero del proyecto y detalle de tarea
    task_engineer_totals = df.groupby(['Task detail', 'Project Engineer'])[['Hours Logged', 'Estimated Hours Logged']].sum()
    task_engineer_totals['Performance Ratio'] = task_engineer_totals['Hours Logged'] / task_engineer_totals['Estimated Hours Logged']

    # Pivotar los datos agrupados para obtener el Performance Ratio total por ingeniero del proyecto y detalle de tarea
    task_engineer_pivot = task_engineer_totals['Performance Ratio'].unstack()

    # Calcular los totales de Hours Logged y Estimated Hours Logged por cada ingeniero del proyecto
    engineer_totals = df.groupby('Project Engineer')[['Hours Logged', 'Estimated Hours Logged']].sum()
    engineer_totals['Performance Ratio'] = engineer_totals['Hours Logged'] / engineer_totals['Estimated Hours Logged']

    # Añadir los totales calculados al pivot
    task_engineer_pivot['Total'] = task_engineer_pivot.mean(axis=1)
    totals_series = engineer_totals['Performance Ratio']
    totals_series['Total'] = (engineer_totals['Hours Logged'].sum() / engineer_totals['Estimated Hours Logged'].sum())

    # Crear un DataFrame con los totales
    totals_df = pd.DataFrame(totals_series).T
    totals_df.index = ['Total']

    # Concatenar los datos con los totales
    task_engineer_pivot = pd.concat([task_engineer_pivot, totals_df])

    # Reordenar las columnas para que la columna 'Total' esté a la derecha
    columns_order = list(task_engineer_pivot.columns)
    task_engineer_pivot = task_engineer_pivot[columns_order]

    # Ordenar las filas de mayor a menor Performance Ratio promedio, manteniendo "Total" al final
    task_engineer_pivot = task_engineer_pivot.sort_values(by='Total', ascending=False)

    # Mover la fila "Total" al final
    total_row = task_engineer_pivot.loc['Total']
    task_engineer_pivot = task_engineer_pivot.drop('Total')
    task_engineer_pivot = pd.concat([task_engineer_pivot, pd.DataFrame(total_row).T])

    # Crear el gráfico de calor usando Plotly
    z = task_engineer_pivot.values
    x = task_engineer_pivot.columns.tolist()
    y = task_engineer_pivot.index.tolist()

    # Crear una máscara para las celdas NaN
    mask = pd.isna(z)

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x,
        y=y,
        colorscale=[
            [0, 'blue'],       # Color para valores bajos (cercanos a 0)
            [0.5, 'white'],    # Color para valores cercanos a 1
            [1, 'red']         # Color para valores altos (mayores a 1)
        ],
        zmin=0,
        zmax=2,
        colorbar=dict(title='Performance Ratio', titleside='right'),
        text=z,  # Añadir los valores de PR como texto
        hoverinfo='text',  # Mostrar los valores de PR en el hover
        showscale=True
    ))

    # Añadir anotaciones para mostrar los valores en cada celda
    annotations = []
    for n, row in enumerate(z):
        for m, val in enumerate(row):
            if not mask[n, m]:  # Añadir anotaciones solo para celdas con valores
                annotations.append(
                    go.layout.Annotation(
                        text=str(round(val, 2)),
                        x=x[m],
                        y=y[n],
                        xref='x1',
                        yref='y1',
                        showarrow=False,
                        font=dict(color='black', size=14)  # Color negro para todos los valores y tamaño de fuente mayor
                    )
                )

    # Añadir celdas grises para valores NaN
    for n, row in enumerate(z):
        for m, val in enumerate(row):
            if mask[n, m]:
                fig.add_shape(
                    type="rect",
                    x0=m-0.5, x1=m+0.5,
                    y0=n-0.5, y1=n+0.5,
                    fillcolor="lightgrey",
                    line=dict(color="lightgrey")
                )

    fig.update_layout(
        title='Heatmap of Performance Ratio by Task Detail and Project Engineer with Averages',
        xaxis_title='Project Engineer and Total',
        yaxis_title='Task Detail and Total',
        annotations=annotations,
        margin=dict(t=50, b=20, l=0, r=0)
    )

    return fig

if __name__ == "__main__":
    fig = create_heatmap4()
    fig.show()

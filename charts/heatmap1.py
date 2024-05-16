import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os

def create_heatmap1():
    # Especificar la ruta completa al archivo CSV
    file_path = os.path.join(os.path.dirname(__file__), 'team_data_Q2.csv')

    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv(file_path)

    # Calcular el nuevo Performance Ratio
    df['Performance Ratio'] = df['Hours Logged'] / df['Estimated Hours Logged']

    # Calcular los totales de Hours Logged y Estimated Hours Logged por cada tipo de planset y detalle de tarea
    task_planset_totals = df.groupby(['Task detail', 'Planset'])[['Hours Logged', 'Estimated Hours Logged']].sum()
    task_planset_totals['Performance Ratio'] = task_planset_totals['Hours Logged'] / task_planset_totals['Estimated Hours Logged']

    # Pivotar los datos agrupados para obtener el Performance Ratio total por tipo de planset y detalle de tarea
    task_planset_pivot = task_planset_totals['Performance Ratio'].unstack()

    # Calcular los totales de Performance Ratio calculados para el DataFrame
    planset_totals = df.groupby('Planset')[['Hours Logged', 'Estimated Hours Logged']].sum()
    planset_totals['Performance Ratio'] = planset_totals['Hours Logged'] / planset_totals['Estimated Hours Logged']

    # Añadir los totales calculados al pivot
    task_planset_pivot.loc['Total'] = planset_totals['Performance Ratio']
    task_planset_pivot['Total'] = task_planset_pivot.mean(axis=1)

    # Reordenar las columnas para que Utility Set esté a la izquierda
    columns_order = ['Utility Set', 'Electrical Permit Set', 'Construction Set', 'Total']
    task_planset_pivot = task_planset_pivot[columns_order]

    # Ordenar las filas de mayor a menor Performance Ratio promedio, manteniendo "Total" al final
    task_planset_pivot = task_planset_pivot.sort_values(by='Total', ascending=False)
    # Mover la fila "Total" al final
    total_row = task_planset_pivot.loc['Total']
    task_planset_pivot = task_planset_pivot.drop('Total')
    task_planset_pivot = pd.concat([task_planset_pivot, pd.DataFrame(total_row).T])

    # Crear el gráfico de calor usando Plotly
    z = task_planset_pivot.values
    x = task_planset_pivot.columns.tolist()
    y = task_planset_pivot.index.tolist()

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
        title='Heatmap of Performance Ratio by Task Detail and Planset Type with Averages',
        xaxis_title='Planset Type and Total',
        yaxis_title='Task Detail and Total',
        annotations=annotations,
        margin=dict(t=50, b=20, l=0, r=0)
    )

    return fig

if __name__ == "__main__":
    fig = create_heatmap1()
    fig.show()

import pandas as pd
import plotly.graph_objects as go
import os

def create_chart():
    # Specify the path to your CSV file
    file_path = os.path.join(os.path.dirname(__file__), 'team_data G2_tipo de costo.csv')

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, encoding='latin1')

    # Verify the existence of the 'Project Engineer' column
    project_engineer_column = 'Project Engineer'
    if project_engineer_column in df.columns:
        # Get the unique Project Engineers
        project_engineers = df[project_engineer_column].unique()

        # Initialize a list to store figures
        figures = []

        for engineer in project_engineers:
            # Filter data for the current Project Engineer
            engineer_data = df[df[project_engineer_column] == engineer]

            # Sum the hours logged by task category
            task_category_summary = engineer_data.groupby('Task Category')['Hours Logged'].sum().reset_index()

            # Create the pie chart using Plotly
            fig = go.Figure()

            fig.add_trace(go.Pie(
                labels=task_category_summary['Task Category'],
                values=task_category_summary['Hours Logged'],
                textinfo='label+percent',
                insidetextorientation='radial',
                marker=dict(colors=['#cc6666', '#3399ff', '#66cc66', '#ff9966', '#9999ff', '#ff66b2', '#99cc66', '#33cccc', '#cc6677', '#ff6666'])
            ))

            # Customize layout
            fig.update_layout(
                title=f'Distribución de Horas Registradas por Categoría de Tarea\n{engineer}',
                margin=dict(t=50, b=20, l=0, r=0),
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=1.1,
                    font=dict(size=16)
                )
            )

            # Append figure to the list
            figures.append(fig)

        # Return the first figure (or handle multiple figures as needed)
        return figures[0]

    else:
        print(f"La columna '{project_engineer_column}' no existe en el archivo CSV.")

if __name__ == "__main__":
    fig = create_chart()
    fig.show()

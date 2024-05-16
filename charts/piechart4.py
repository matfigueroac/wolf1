import pandas as pd
import plotly.graph_objects as go
import os

def create_chart():
    # Specify the path to your CSV file
    file_path = os.path.join(os.path.dirname(__file__), 'team_data G2_tipo de costo.csv')

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, encoding='latin1')

    # Sum the hours logged by task type
    task_type_summary = df.groupby('Planset/Task Type')['Hours Logged'].sum().sort_values(ascending=False)

    # Get the percentage of each task type
    task_type_percentage = (task_type_summary / task_type_summary.sum()) * 100

    # Define colors for each category
    category_colors = {
        'Engineering': ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c'] * 2,
        'Management': ['#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2'] * 2,
        'Projects': ['#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d'] * 2,
        'Other': ['#17becf', '#9edae5'] * 2
    }

    # Map task types to categories
    task_categories = {
        'Engineering review': 'Engineering',
        'Engineering Library': 'Engineering',
        'Planset Template Improvements': 'Engineering',
        'Control Revision': 'Engineering',
        'Training': 'Engineering',
        'Meeting': 'Management',
        'Emails': 'Management',
        'Slack': 'Management',
        'Smartsheet': 'Management',
        'Weekly Timesheet': 'Management',
        'Sheets Template Improvements': 'Management',
        'Hours log input': 'Management',
        'ASANA': 'Management',
        'Utility Set': 'Projects',
        'Electrical Permit Set': 'Projects',
        'Construction Set': 'Projects',
        'As Built Set': 'Projects',
        'Rest / Stretch / Walk': 'Other',
        'Lunch': 'Other',
        'Day off': 'Other',
        'Quotation': 'Engineering'
    }

    # Assign colors based on categories
    colors = []
    for task in task_type_summary.index:
        category = task_categories.get(task, 'Other')
        if category in category_colors and category_colors[category]:
            colors.append(category_colors[category].pop(0))
        else:
            # If no colors are available, add a default color
            colors.append('#d3d3d3')

    # Prepare labels with categories
    labels = [f'{label} ({task_categories.get(label, "Other")})' for label in task_type_summary.index]

    # Create the pie chart using Plotly
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=task_type_summary,
        textinfo='label+percent',
        insidetextorientation='radial',
        marker=dict(colors=colors)
    ))

    # Customize layout
    fig.update_layout(
        title='Distribución de % uso horas totales por Task Type',
        margin=dict(t=50, b=20, l=0, r=0),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.1,
            font=dict(size=12)
        )
    )

    return fig

if __name__ == "__main__":
    fig = create_chart()
    fig.show()

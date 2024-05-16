from flask import Flask
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import charts

server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Interactive Dashboard", className="text-center mb-4"), width=12)
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='chart-dropdown',
                    options=[
                        {'label': 'Bar Chart 0: Total Hours Logged by Task Category', 'value': 'barchart0'},
                        {'label': 'Bar Chart 1: Total Hours Logged by Planset Type', 'value': 'barchart1'},
                        {'label': 'Bar Chart 2: Total Hours Logged by Project Category', 'value': 'barchart2'},
                        {'label': 'Bar Chart 3: Total Hours Logged by Cost Type', 'value': 'barchart3'},
                        {'label': 'Pie Chart 0: Hours Distribution by Task Category', 'value': 'piechart0'},
                        {'label': 'Pie Chart 1: Hours Distribution by Planset Type', 'value': 'piechart1'},
                        {'label': 'Pie Chart 2: Hours Distribution by Project Engineer', 'value': 'piechart2'},
                        {'label': 'Pie Chart 3: Hours Distribution by Task Category for Felipe Figueroa', 'value': 'piechart3'},
                        {'label': 'Pie Chart 4: Hours Distribution by Task Type', 'value': 'piechart4'},
                        {'label': 'Heatmap 0: Performance Ratio by Project Name and Planset Type', 'value': 'heatmap0'},
                        {'label': 'Heatmap 1: Performance Ratio by Task Detail and Planset Type', 'value': 'heatmap1'},
                        {'label': 'Heatmap 2: Performance Ratio by Task Detail and Project Category', 'value': 'heatmap2'},
                        {'label': 'Heatmap 3: Performance Ratio by Task Detail and PV AC Power KW Range', 'value': 'heatmap3'},
                        {'label': 'Heatmap 4: Performance Ratio by Task Detail and Project Engineer', 'value': 'heatmap4'},
                    ],
                    value='barchart0',
                    className="mb-4"
                ), width=12
            )
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id='chart-output'), width=12)
        )
    ],
    fluid=True,
    className="dbc"
)

@app.callback(
    Output('chart-output', 'figure'),
    [Input('chart-dropdown', 'value')]
)
def update_chart(chart_name):
    if chart_name == 'barchart0':
        return charts.create_barchart0()
    elif chart_name == 'barchart1':
        return charts.create_barchart1()
    elif chart_name == 'barchart2':
        return charts.create_barchart2()
    elif chart_name == 'barchart3':
        return charts.create_barchart3()
    elif chart_name == 'piechart0':
        return charts.create_piechart0()
    elif chart_name == 'piechart1':
        return charts.create_piechart1()
    elif chart_name == 'piechart2':
        return charts.create_piechart2()
    elif chart_name == 'piechart3':
        return charts.create_piechart3()
    elif chart_name == 'piechart4':
        return charts.create_piechart4()
    elif chart_name == 'heatmap0':
        return charts.create_heatmap0()
    elif chart_name == 'heatmap1':
        return charts.create_heatmap1()
    elif chart_name == 'heatmap2':
        return charts.create_heatmap2()
    elif chart_name == 'heatmap3':
        return charts.create_heatmap3()
    elif chart_name == 'heatmap4':
        return charts.create_heatmap4()

if __name__ == '__main__':
    app.run_server(debug=True)

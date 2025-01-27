# dashboard.py

import os
import json
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go

def find_log_files(folder="logs"):
    """
    Returns a sorted list of .json files in the specified folder 
    whose names match 'metrics_log_*.json'.
    """
    if not os.path.exists(folder):
        return []
    files = []
    for f in os.listdir(folder):
        if f.startswith("metrics_log_") and f.endswith(".json"):
            files.append(f)
    return sorted(files)

app = dash.Dash(__name__)
app.title = "AI Model Performance Dashboard"

app.layout = html.Div([
    html.H1("AI Model Performance Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select a log file:"),
        dcc.Dropdown(
            id='log-file-dropdown',
            options=[{'label': fname, 'value': fname} for fname in find_log_files()],
            value=None,
            placeholder="Choose a log file from the logs/ folder"
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    html.Br(),
    html.Div(id='file-info', style={'textAlign': 'center', 'fontWeight': 'bold'}),

    dcc.Graph(id='inference-time-graph'),
    dcc.Graph(id='cpu-usage-graph'),
    # Optionally, you could add another graph for memory usage if you log it
])

@app.callback(
    [Output('file-info', 'children'),
     Output('inference-time-graph', 'figure'),
     Output('cpu-usage-graph', 'figure')],
    [Input('log-file-dropdown', 'value')]
)
def update_graphs(selected_file):
    """
    When the user selects a file from the dropdown, load its JSON logs 
    and update the two plots (inference time & CPU usage).
    """
    if not selected_file:
        # No file chosen => return empty placeholders
        empty_fig = go.Figure()
        return ("No file selected.", empty_fig, empty_fig)

    file_path = os.path.join("logs", selected_file)
    if not os.path.isfile(file_path):
        empty_fig = go.Figure()
        return (f"File not found: {file_path}", empty_fig, empty_fig)

    # Load the JSON logs
    with open(file_path, 'r') as f:
        logs = json.load(f)

    # Extract data for plotting
    iterations = [entry["iteration"] for entry in logs]
    inference_times = [entry["inference_time"] for entry in logs]
    cpu_before = [entry["before"]["cpu_percent"] for entry in logs]
    cpu_after = [entry["after"]["cpu_percent"] for entry in logs]
    # If you want memory usage, you can also extract entry["before"]["memory_percent"], etc.

    # Plot inference time
    fig_inference = go.Figure()
    fig_inference.add_trace(go.Scatter(
        x=iterations,
        y=inference_times,
        mode='lines+markers',
        name='Inference Time (s)'
    ))
    fig_inference.update_layout(
        title="Inference Time per Iteration",
        xaxis_title="Iteration",
        yaxis_title="Time (seconds)"
    )

    # Plot CPU usage
    fig_cpu = go.Figure()
    fig_cpu.add_trace(go.Scatter(
        x=iterations,
        y=cpu_before,
        mode='lines+markers',
        name='CPU Before (%)',
        line=dict(color='blue')
    ))
    fig_cpu.add_trace(go.Scatter(
        x=iterations,
        y=cpu_after,
        mode='lines+markers',
        name='CPU After (%)',
        line=dict(color='red')
    ))
    fig_cpu.update_layout(
        title="CPU Usage Before & After Inference",
        xaxis_title="Iteration",
        yaxis_title="CPU Usage (%)"
    )

    file_info = f"Currently displaying: {selected_file}"
    return (file_info, fig_inference, fig_cpu)

if __name__ == '__main__':
    app.run_server(debug=True)

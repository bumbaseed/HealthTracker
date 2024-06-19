import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output
from visualization import extract_data, find_common_user_id

# Initialize the Dash app
app = dash.Dash(__name__)

# Find a common user ID
user_id = find_common_user_id()
if not user_id:
    raise ValueError("No common user ID found in both datasets. Ensure data exists for a user in both datasets.")

# Load data for the specific user
merged_df = extract_data(user_id)

# Define the initial start and end dates
initial_start_date = merged_df['Day'].min()
initial_end_date = merged_df['Day'].max()

# Define the layout of the app
app.layout = html.Div([
    html.H1("Personal Health Dashboard"),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=initial_start_date,
        end_date=initial_end_date,
        display_format='YYYY-MM-DD'
    ),
    dcc.Graph(id='heart-rate-graph'),
    dcc.Graph(id='sleep-stage-graph')
])

# Define the callback to update graphs
@app.callback(
    [Output('heart-rate-graph', 'figure'),
     Output('sleep-stage-graph', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graphs(start_date, end_date):
    # Use the entire date range if start_date or end_date is None
    if start_date is None:
        start_date = initial_start_date
    if end_date is None:
        end_date = initial_end_date

    print(f"Filtering data from {start_date} to {end_date}")
    
    filtered_df = merged_df[(merged_df['Day'] >= start_date) & (merged_df['Day'] <= end_date)]
    
    heart_rate_fig = {
        'data': [{'x': filtered_df['Day'], 'y': filtered_df['AvgHeartRate'], 'type': 'line', 'name': 'AvgHeartRate'}],
        'layout': {'title': 'Average Heart Rate Over Time'}
    }
    
    sleep_stage_fig = {
        'data': [{'x': filtered_df['Day'], 'y': filtered_df['value'], 'type': 'line', 'name': 'SleepStage'}],
        'layout': {'title': 'Sleep Stages Over Time'}
    }
    
    print("Filtered data:")
    print(filtered_df.head())
    
    return heart_rate_fig, sleep_stage_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



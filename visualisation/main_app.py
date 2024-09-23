import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from visualisation.weather_data import load_histo_weather_data_station

# Load the CSV data
df = load_histo_weather_data_station(59343001)

# Ensure DATE is parsed and set as the index
df["DATE"] = pd.to_datetime(df["DATE"])
df.set_index("DATE", inplace=True)

# Initialize the Dash app
app = Dash(__name__)

# Get the list of columns for dropdown options
columns = df.columns  # Exclude the first column which is likely an ID or date

# Define the layout of the app
app.layout = html.Div(
    [
        html.H1("Weather Data Visualization"),
        html.Div(
            [
                html.Label("Select Variables:"),
                dcc.Dropdown(
                    id="variables-dropdown",
                    options=[{"label": col, "value": col} for col in columns],
                    value=[columns[0], columns[1]],  # Default values
                    multi=True,
                ),
            ]
        ),
        dcc.Graph(id="variable-graph"),
        html.H1("Weather Data Correlation"),
        html.Div(
            [
                html.Label("Select Variable 1 for Correlation:"),
                dcc.Dropdown(
                    id="correlation-variable1-dropdown",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[0],  # Default value
                ),
            ]
        ),
        html.Div(
            [
                html.Label("Select Variable 2 for Correlation:"),
                dcc.Dropdown(
                    id="correlation-variable2-dropdown",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[1],  # Default value
                ),
            ]
        ),
        dcc.Graph(id="correlation-graph"),
    ]
)


# Define the callback to update the graphs
@app.callback(
    [Output("variable-graph", "figure"), Output("correlation-graph", "figure")],
    [
        Input("variables-dropdown", "value"),
        Input("correlation-variable1-dropdown", "value"),
        Input("correlation-variable2-dropdown", "value"),
    ],
)
def update_graphs(variables, corr_var1, corr_var2):
    # Create the figure for the selected variables
    data = [
        {"x": df.index, "y": df[var], "type": "line", "name": var} for var in variables
    ]
    variable_fig = {
        "data": data,
        "layout": {"title": "Selected Variables Over Time", "xaxis": {"title": "DATE"}},
    }

    # Create the figure for the correlation between the selected variables
    correlation_fig = {
        "data": [
            {
                "x": df[corr_var1],
                "y": df[corr_var2],
                "mode": "markers",
                "name": f"{corr_var1} vs {corr_var2}",
            }
        ],
        "layout": {
            "title": f"Correlation between {corr_var1} and {corr_var2}",
            "xaxis": {"title": corr_var1},
            "yaxis": {"title": corr_var2},
        },
    }

    return variable_fig, correlation_fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

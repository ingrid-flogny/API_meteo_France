import pandas as pd
from dash import Dash
from dash.dependencies import Input, Output

from visualisation.weather_data import filter_dataframe_by_poste


def callbacks_app_visualisation(app: Dash, df: pd.DataFrame):
    @app.callback(
        Output("variable-graph", "figure"),
        [Input("station-id-dropdown", "value"), Input("variables-dropdown", "value")],
    )
    def update_variable_graph(station_id: str, variables: list):
        # Load data for the selected station
        filtered_df = filter_dataframe_by_poste(df, station_id)

        # Create the figure for the selected variables
        data = [
            {"x": filtered_df.index, "y": filtered_df[var], "type": "line", "name": var}
            for var in variables
        ]
        variable_fig = {
            "data": data,
            "layout": {
                "title": "Selected Variables Over Time",
                "xaxis": {"title": "DATE"},
            },
        }
        return variable_fig

    @app.callback(
        Output("correlation-graph", "figure"),
        [
            Input("correlation-variable1-dropdown", "value"),
            Input("correlation-variable2-dropdown", "value"),
        ],
    )
    def update_correlation_graph(corr_var1, corr_var2):
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
        return correlation_fig

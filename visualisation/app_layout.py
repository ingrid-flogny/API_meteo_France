from dash import Dash, dcc, html
from dash.dependencies import Input, Output


def app_visualisation_layout(columns: list) -> html.Div:
    return html.Div(
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

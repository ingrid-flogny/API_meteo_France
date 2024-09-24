import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from visualisation.app_callbacks import callbacks_app_visualisation
from visualisation.app_layout import app_visualisation_layout
from visualisation.weather_data import load_histo_weather_data_all_stations

# Load the CSV data
df = load_histo_weather_data_all_stations()

# Ensure DATE is parsed and set as the index
df["DATE"] = pd.to_datetime(df["DATE"])
df.set_index("DATE", inplace=True)

# Initialize the Dash app
app = Dash(__name__)

# Get the list of columns for dropdown options
columns = df.columns

# Define the layout of the app
app.layout = app_visualisation_layout(df)

# Define the callbacks for the app
callbacks_app_visualisation(app, df)


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

import pandas as pd
import os

from config import PROJECT_ROOT
from utils import from_station_number_to_histo_file_path

"""=====================================================================================================
    Load data
===================================================================================================="""


def load_histo_weather_data_all_stations() -> pd.DataFrame:
    """
    Load the historical data of all stations.
    :return:
    """
    file_path = PROJECT_ROOT + "/data_meteo_histo/stations_weather_data_histo.csv"
    df = pd.read_csv(file_path, delimiter=";", decimal=",")
    return df


def load_histo_weather_data_station(station_number: str) -> pd.DataFrame:
    """
    Get the historical data of a station from the CSV file.
    :param station_number:
    :return:
    """
    file_path = from_station_number_to_histo_file_path(station_number)
    df = pd.read_csv(file_path, delimiter=";", decimal=",")
    return df


"""=====================================================================================================
    Get stations IDs
===================================================================================================="""


def get_all_stations_ids_retrieved() -> list:
    """
    Get the list of all station IDs. Stations whose data has been retrieved in data_meteo_histo folder.
    :return:
    """
    # Get the list of all station numbers
    stations = os.listdir(PROJECT_ROOT + "/data_meteo_histo/")
    stations = [int(station) for station in stations]
    return stations


def get_unique_station_ids(df: pd.DataFrame) -> list:
    """
    Get the unique station IDs from the DataFrame.

    :param df: DataFrame containing weather data
    :return: List of unique station IDs
    """
    unique_station_ids = df["POSTE"].unique().tolist()
    return unique_station_ids


"""=====================================================================================================
    Filter data
===================================================================================================="""


def filter_dataframe_by_poste(df: pd.DataFrame, poste_value: str) -> pd.DataFrame:
    """
    Filter the DataFrame by the 'POSTE' column.
    :param df:
    :param poste_value:
    :return:
    """
    if "POSTE" not in df.columns:
        raise ValueError("The DataFrame does not contain a 'POSTE' column.")

    filtered_df = df[df["POSTE"] == poste_value]
    return filtered_df

import pandas as pd
import os

from config import PROJECT_ROOT
from utils import from_station_number_to_histo_file_path

"""=====================================================================================================
    Load data
===================================================================================================="""


def load_histo_weather_data_station(station_number: int) -> pd.DataFrame:
    """
    Get the historical data of a station from the CSV file.
    :param station_number:
    :return:
    """
    file_path = from_station_number_to_histo_file_path(station_number)
    df = pd.read_csv(file_path, delimiter=";", decimal=",")
    return df


"""=====================================================================================================

===================================================================================================="""


def get_all_stations_ids_retrieved() -> list:
    """
    Get the list of all retrieved station IDs.
    :return:
    """
    # Get the list of all station numbers
    stations = os.listdir(PROJECT_ROOT + "/data_meteo_histo/")
    stations = [int(station) for station in stations]
    return stations

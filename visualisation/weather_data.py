import pandas as pd

from utils import from_station_number_to_histo_file_path


def load_histo_weather_data_station(station_number: int) -> pd.DataFrame:
    """
    Get the historical data of a station from the CSV file.
    :param station_number:
    :return:
    """
    file_path = from_station_number_to_histo_file_path(station_number)
    df = pd.read_csv(file_path, delimiter=";", decimal=",")
    return df

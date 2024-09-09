import urllib.parse
import os
import pandas as pd
from datetime import datetime
from logs.logging_config import logger

"""=====================================================================================================
Date formats
====================================================================================================="""
# From iso date to str date
def extract_date(encoded_date: str) -> str:
    """
    Extract the date str from the encoded date ISO format.
    :param encoded_date:
    :return:
    """
    decoded_date = urllib.parse.unquote(encoded_date)
    parsed_date = datetime.strptime(decoded_date, "%Y-%m-%dT%H:%M:%SZ")
    return parsed_date.strftime("%Y-%m-%d")

# From str date to iso date
def convert_date_to_iso(date_str: str) -> str:
    """
    Convert the date str to the ISO format.
    :param date_str:
    :return:
    """
    # Parse the input date string
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    # Format the date to the desired ISO format
    formatted_date = date_obj.strftime('%Y-%m-%dT%H%%3A%M%%3A%SZ')

    return formatted_date

"""=====================================================================================================
Folder management
====================================================================================================="""
def ensure_folder_exists(folder_path: str):
    """
    Ensure that the folder exists. If not, create it.
    :param folder_path:
    :return:
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.info(f"Folder created: {folder_path}")
    else:
        pass


"""=====================================================================================================
Files names
====================================================================================================="""

def from_station_histo_file_name_to_station_number(file_name: str) -> int:
    """
    Get the station number from the historical file name.
    :param file_name:
    :return:
    """
    # Extract the base name of the file
    base_name = os.path.basename(file_name)

    station_number_str = base_name.split('_')[0]
    return int(station_number_str)

"""=====================================================================================================
Path names
====================================================================================================="""

def from_station_number_to_histo_file_path(station_number: int) -> str:
    """
    Get the file path for the final historical data of a station.
    :param station_number:
    :return:
    """
    file_path = f"data_meteo_histo/{station_number}/{station_number}_histo.csv"
    return file_path

def from_date_start_end_to_path_name(station_number:int, date_start: str, date_end: str) -> str:
    """
    Get the file path for the historical data of a station on a given date range.
    :param station_number:
    :param date_start:
    :param date_end:
    :return:
    """
    file_name = f"data_meteo_histo/{station_number}/from{date_start}_to{date_end}.csv"
    return file_name


"""=====================================================================================================
CSV HISTO
====================================================================================================="""

def get_station_histo_df_from_csv(station_number: int) -> pd.DataFrame:
    """
    Get the historical data of a station from the CSV file.
    :param station_number:
    :return:
    """
    file_path = from_station_number_to_histo_file_path(station_number)
    df = pd.read_csv(file_path, sep=';', parse_dates=[1], dayfirst=True)
    return df
import urllib.parse
import os
from datetime import datetime
from logs.logging_config import logger

"""=====================================================================================================
Date formats
====================================================================================================="""
# From iso date to str date
def extract_date(encoded_date: str) -> str:
    decoded_date = urllib.parse.unquote(encoded_date)
    parsed_date = datetime.strptime(decoded_date, "%Y-%m-%dT%H:%M:%SZ")
    return parsed_date.strftime("%Y-%m-%d")

# From str date to iso date
def convert_date_to_iso(date_str: str) -> str:
    # Parse the input date string
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    # Format the date to the desired ISO format
    formatted_date = date_obj.strftime('%Y-%m-%dT%H%%3A%M%%3A%SZ')

    return formatted_date

"""=====================================================================================================
Folder management
====================================================================================================="""
def ensure_folder_exists(folder_path: str):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.info(f"Folder created: {folder_path}")
    else:
        pass


"""=====================================================================================================
Files names
====================================================================================================="""
def from_station_number_to_histo_file_path(station_number: int) -> str:
    file_path = f"data_meteo_histo/{station_number}/{station_number}_histo.csv"
    return file_path


def from_station_histo_file_name_to_station_number(file_name: str) -> int:
    # Extract the base name of the file
    base_name = os.path.basename(file_name)

    station_number_str = base_name.split('_')[0]
    return int(station_number_str)

def from_date_start_end_to_file_name(date_start: str, date_end: str) -> str:
    file_name = f"from{date_start}_to{date_end}.csv"
    return file_name

def from_date_start_end_to_path_name(station_number:int, date_start: str, date_end: str) -> str:
    file_name = f"data_meteo_histo/{station_number}/from{date_start}_to{date_end}.csv"
    return file_name
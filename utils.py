import urllib.parse
import os
import pandas as pd
from datetime import datetime

from config import PROJECT_ROOT
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
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Format the date to the desired ISO format
    formatted_date = date_obj.strftime("%Y-%m-%dT%H%%3A%M%%3A%SZ")

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
Path names
====================================================================================================="""


# Path to station histo file
def from_station_number_to_histo_file_path(station_number: str) -> str:
    """
    Get the file path for the final historical data of a station.
    :param station_number:
    :return:
    """
    file_path = (
        PROJECT_ROOT + f"/data_meteo_histo/{station_number}/{station_number}_histo.csv"
    )
    return file_path


# Path weather data per year
def from_date_start_end_to_path_name(
    station_number: str, date_start: str, date_end: str
) -> str:
    """
    Get the file path for the historical data of a station on a given date range.
    :param station_number:
    :param date_start:
    :param date_end:
    :return:
    """
    file_name = (
        PROJECT_ROOT
        + f"/data_meteo_histo/{station_number}/from{date_start}_to{date_end}.csv"
    )
    return file_name


"""=====================================================================================================
Dataframe CSV HISTO
====================================================================================================="""


def get_station_histo_df(station_number: str) -> pd.DataFrame:
    """
    Get the historical data of a station from the CSV file.
    :param station_number:
    :return:
    """
    file_path = from_station_number_to_histo_file_path(station_number)
    df = pd.read_csv(file_path, sep=";", parse_dates=[1], dayfirst=True)
    return df


"""=====================================================================================================
    Weather data columns
====================================================================================================="""


def rename_columns_using_mapping(description_file_path: str, histo_file_path: str):
    """
    Rename the columns in the historical data file using the mapping in the description file.
    :param description_file_path:
    :param histo_file_path:
    :return:
    """
    # Step 1: Read the description_variables_meteo.csv file to create a mapping
    description_df = pd.read_csv(description_file_path, sep=";")
    mnemonique_to_libelle = dict(
        zip(description_df["Mnémonique"], description_df["Libellé"])
    )

    # Step 2: Read the 59343001_histo.csv file
    histo_df = pd.read_csv(histo_file_path, sep=";")

    # Step 3: Rename the columns in 59343001_histo.csv using the mapping
    histo_df.rename(columns=mnemonique_to_libelle, inplace=True)

    # Step 4: Save the updated DataFrame back to the CSV file
    histo_df.to_csv(histo_file_path, sep=";", index=False)


def filter_columns_histo_file(
    input_histo_file_path: str, output_histo_file_path: str, columns_to_keep: list
):
    """
    Filter the columns in the historical data file.
    :param histo_file_path:
    :param columns_to_keep:
    :return:
    """
    # Read the CSV file
    df = pd.read_csv(input_histo_file_path, sep=";")

    # Filter the columns
    df = df[columns_to_keep]

    # Save the updated DataFrame back to the CSV file
    df.to_csv(output_histo_file_path, sep=";", index=False)

    logger.info(f"Columns filtered in {output_histo_file_path}")

    return True

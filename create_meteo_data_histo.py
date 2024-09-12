import os
import pandas as pd
import time

from logs.logging_config import logger
from CSVDownloader import CSVDownloader
from utils import (
    extract_date,
    convert_date_to_iso,
    from_station_number_to_histo_file_path,
    from_date_start_end_to_path_name,
    get_station_histo_df_from_csv,
)

"""=======================================================================================================================

Création des données météo historiques pour une station : 1 fichier par année et par station

========================================================================================================================"""
date_start_end = {
    "2017-01-01T00%3A00%3A00Z": "2018-01-01T00%3A00%3A00Z",
    "2018-01-01T00%3A00%3A00Z": "2019-01-01T00%3A00%3A00Z",
    "2019-01-01T00%3A00%3A00Z": "2020-01-01T00%3A00%3A00Z",
    "2020-01-01T00%3A00%3A00Z": "2021-01-01T00%3A00%3A00Z",
    "2021-01-01T00%3A00%3A00Z": "2022-01-01T00%3A00%3A00Z",
    "2022-01-01T00%3A00%3A00Z": "2023-01-01T00%3A00%3A00Z",
    "2023-01-01T00%3A00%3A00Z": "2024-01-01T00%3A00%3A00Z",
    "2024-01-01T00%3A00%3A00Z": "2024-09-11T00%3A00%3A00Z",
}


def download_data_date(station_number: int, date_start: str, date_end: str) -> bool:
    """
    Download the historical weather data for a station for a given date range.
    :param station_number:
    :param date_start: Date ISO format
    :param date_end: Date ISO format
    :return:
    """
    downloader = CSVDownloader(
        num_station=station_number, date_start=date_start, date_end=date_end
    )

    retry_count = 0
    max_retries = 10
    while not downloader.download_is_complete and retry_count < max_retries:
        downloader.run()
        retry_count += 1
        if downloader.download_is_complete:
            logger.info(
                f"Download successful for station {station_number} from {date_start} to {date_end}"
            )
            return True
        else:
            logger.warning(
                f"Download attempt {retry_count} failed for station {station_number} from {date_start} to {date_end}"
            )

    logger.error(
        f"Failed to download data for station {station_number} from {date_start} to {date_end} after {max_retries} attempts"
    )
    return False


def download_histo_per_station(num_station: int) -> bool:
    """
    Loop to download all historical data files for a station.
    Date ranges are defined in the date_start_end dictionary.
    :param num_station:
    :return:
    """
    for date_start, date_end in date_start_end.items():
        return download_data_date(num_station, date_start, date_end)


def verify_files_histo_all_exist(num_station: int) -> bool:
    """
    Check if all historical weather data files exist for a station.
    Date ranges are defined in the date_start_end dictionary.
    :param num_station:
    :return:
    """
    for date_start, date_end in date_start_end.items():
        file_path = (
            f"data_meteo_histo/{num_station}/from{extract_date(date_start)}_"
            f"to{extract_date(date_end)}.csv"
        )
        if not os.path.isfile(file_path):
            logger.info(f"File {file_path} does not exist.")
            download_data_date(num_station, date_start, date_end)

    logger.info(f"All files for station {num_station} exist. Checking OK")
    return True


"""=====================================================================================================

Agglomération des données météo historiques pour une station : 1 fichier par station

========================================================================================================="""


def aggregate_histo_data(num_station: int) -> bool:
    """
    Aggregate all historical weather data files for a station into a single file.
    The final format is a CSV file : num_station_histo.csv
    :param num_station:
    :return:
    """
    station_folder = f"data_meteo_histo/{num_station}"
    station_files = os.listdir(station_folder)
    station_files.sort()
    if len(station_files) == 0:
        raise FileNotFoundError(
            f"No files found for station {num_station} in folder {station_folder}"
        )

    # Create the output file
    station_histo_file_path = from_station_number_to_histo_file_path(num_station)
    with open(station_histo_file_path, "w") as output:
        # Write the header
        with open(f"{station_folder}/{station_files[0]}", "r") as first_file:
            header = first_file.readline()
            output.write(header)

        # Write the data
        for file in station_files:
            with open(f"{station_folder}/{file}", "r") as input_file:
                # Skip the header
                input_file.readline()
                for line in input_file:
                    output.write(line)

    logger.info(
        f"Aggregation complete for station {num_station}. File saved to {station_histo_file_path}"
    )
    return True


"""========================================================================================================

Quality check for the aggregated historical data files

=============================================================================================================="""


def check_duplicated_dates(num_station: int) -> bool:
    """
    Check for duplicate dates in the final historical data file of a station.
    :param num_station:
    :return:
    """
    # Load station data histo file
    df = get_station_histo_df_from_csv(num_station)
    dates = df.iloc[:, 1]

    # Check for duplicate dates
    duplicated_dates = dates[dates.duplicated()]
    station_histo_file_path = from_station_number_to_histo_file_path(num_station)
    if not duplicated_dates.empty:
        logger.error(
            f"Duplicate dates found in the file {station_histo_file_path}: {duplicated_dates.tolist()}"
        )
        return False
    logger.info(f"No duplicate dates found in the file {station_histo_file_path}")
    return True


def check_missing_dates(num_station: int) -> bool:
    """
    Check for missing dates in the final historical data file of a station.
    Check for missing dates between min date and max date.
    :param num_station:
    :return:
    """
    # Load station data histo file
    df = get_station_histo_df_from_csv(num_station)
    dates = df.iloc[:, 1]
    station_histo_file_path = from_station_number_to_histo_file_path(num_station)

    # Check if dates are already in datetime format
    if not pd.api.types.is_datetime64_any_dtype(dates):
        dates = pd.to_datetime(dates, format="%Y-%m-%d", errors="coerce")
    date_range = pd.date_range(start=dates.min(), end=dates.max())
    missing_dates = date_range[~date_range.isin(dates)]

    # Check for missing dates
    if not missing_dates.empty:
        missing_dates = missing_dates.strftime("%Y-%m-%d").tolist()
        logger.info(
            f"Missing dates found in the file {station_histo_file_path}: {missing_dates}"
        )
        return False

    logger.info(f"No missing dates found in the file {station_histo_file_path}")
    return True


def verify_data_quality_in_histo_files(num_station: int) -> bool:
    """
    Verify the quality of the final historical data files for a station.
    Quality checks : duplicates and missing dates.
    :param num_station:
    :return:
    """
    station_histo_file_path = from_station_number_to_histo_file_path(num_station)

    if not os.path.isfile(station_histo_file_path):
        logger.error(f"Aggregated file {station_histo_file_path} does not exist.")
        return False

    # Check for duplicate dates
    if not check_duplicated_dates(num_station):
        drop_date_duplicates(num_station)

    # Check for missing dates
    while not check_missing_dates(num_station):
        download_and_add_data_missing_dates(num_station)
        time.sleep(3)

    if check_duplicated_dates(num_station) and check_missing_dates(num_station):
        logger.info(
            f"Data quality check passed for files {station_histo_file_path}: No duplicate or missing dates."
        )
        return True
    else:
        return False


"""======================================================================================================================

Repairing historical data files

==========================================================================================================================="""


def drop_date_duplicates(station_number: int) -> bool:
    """
    Drop duplicate dates in the final historical data file of a station.
    :param station_number:
    :return:
    """
    # Load station data histo file
    df = get_station_histo_df_from_csv(station_number)
    dates = df.iloc[:, 1]

    # Check for duplicate dates
    duplicated_dates = dates[dates.duplicated()]
    station_histo_file_path = from_station_number_to_histo_file_path(station_number)

    # Drop the duplicates
    if not duplicated_dates.empty:
        df.drop_duplicates(subset="DATE", inplace=True)
        df.to_csv(station_histo_file_path, sep=";", index=False)
        logger.info(f"Duplicates removed from file {station_histo_file_path}")
    return True


def add_date_to_histo_file(file_paths: list, station_number: int) -> bool:
    """
    Add the data from a list of files to the aggregated final historical data file of a station.
    Add the data from files like from2017-01-01_to2018-01-01.csv to the final file 59343001_histo.csv
    :param file_paths:
    :param station_number:
    :return:
    """
    histo_file = from_station_number_to_histo_file_path(station_number)

    if not histo_file:
        raise ValueError("No files provided for aggregation")

    # Read the existing historical file into a DataFrame
    if os.path.exists(histo_file):
        histo_df = pd.read_csv(histo_file, sep=";", parse_dates=[1], dayfirst=True)
    else:
        histo_df = pd.DataFrame()

    # Append the data from all files
    for file_path in file_paths:
        df = pd.read_csv(file_path, sep=";", parse_dates=[1], dayfirst=True)
        histo_df = pd.concat([histo_df, df], ignore_index=True)
        histo_df["DATE"] = pd.to_datetime(
            histo_df["DATE"], format="%Y-%m-%d", errors="coerce"
        )

    # Remove any empty lines
    histo_df.dropna(how="all", inplace=True)

    # Save the DataFrame back to the CSV file
    histo_df.to_csv(histo_file, sep=";", index=False)

    logger.info(f"Aggregation complete. File saved to {histo_file}")

    return True


def download_and_add_data_missing_dates(num_station: int) -> bool:
    """
    Download the missing data files for a station and add them to the aggregated final historical data file.
    One file per missing date. One file is like from2017-01-01_to2017-01-01.csv
    :param num_station:
    :return:
    """
    # Load station data histo file
    df = get_station_histo_df_from_csv(num_station)
    dates = df.iloc[:, 1]
    station_histo_file_path = from_station_number_to_histo_file_path(num_station)

    # Check if dates are already in datetime format
    if not pd.api.types.is_datetime64_any_dtype(dates):
        dates = pd.to_datetime(dates, format="%Y-%m-%d", errors="coerce")
    date_range = pd.date_range(start=dates.min(), end=dates.max())
    missing_dates = date_range[~date_range.isin(dates)]

    if not missing_dates.empty:
        for date in missing_dates:
            date_iso = convert_date_to_iso(date.strftime("%Y-%m-%d"))

            # Download the missing data
            download_data_date(num_station, date_iso, date_iso)

    # Add the missing data to the aggregated file
    list_file_paths = [
        from_date_start_end_to_path_name(
            num_station, date_iso.strftime("%Y-%m-%d"), date_iso.strftime("%Y-%m-%d")
        )
        for date_iso in missing_dates
    ]
    add_date_to_histo_file(list_file_paths, num_station)

    logger.info(
        f"Missing dates files downloaded and added to {station_histo_file_path}"
    )

    return True

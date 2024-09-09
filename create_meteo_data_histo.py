import os
import pandas as pd
import time

from logs.logging_config import logger
from CSVDownloader import CSVDownloader
from utils import extract_date, convert_date_to_iso, from_station_histo_file_name_to_station_number, \
    from_station_number_to_histo_file_path, from_date_start_end_to_path_name

"""==============================================================================================================

Création des données météo historiques pour une station : 1 fichier par année et par station

========================================================================================================================"""
date_start_end= {
    "2017-01-01T00%3A00%3A00Z": "2018-01-01T00%3A00%3A00Z",
    "2018-01-01T00%3A00%3A00Z": "2019-01-01T00%3A00%3A00Z",
    "2019-01-01T00%3A00%3A00Z": "2020-01-01T00%3A00%3A00Z",
    "2020-01-01T00%3A00%3A00Z": "2021-01-01T00%3A00%3A00Z",
    "2021-01-01T00%3A00%3A00Z": "2022-01-01T00%3A00%3A00Z",
    "2022-01-01T00%3A00%3A00Z": "2023-01-01T00%3A00%3A00Z",
    "2023-01-01T00%3A00%3A00Z": "2024-01-01T00%3A00%3A00Z",
    "2024-01-01T00%3A00%3A00Z": "2024-09-05T00%3A00%3A00Z",
}

def download_histo_per_station(num_station: int):
    for date_start, date_end in date_start_end.items():
        downloader = CSVDownloader(
            num_station=num_station,
            date_start=date_start,
            date_end=date_end
        )
        downloader.run()

def verify_files_histo_all_exist(num_station: int):
    for date_start, date_end in date_start_end.items():
        file_path = (
            f"data_meteo_histo/{num_station}/from{extract_date(date_start)}_"
            f"to{extract_date(date_end)}.csv"
        )
        if not os.path.isfile(file_path):
            logger.info(f"File {file_path} does not exist.")
            downloader = CSVDownloader(
                num_station=num_station,
                date_start=date_start,
                date_end=date_end
            )
            # Launch download : try at most 5 times
            retry_count = 0
            while not downloader.download_is_complete and retry_count < 5:
                downloader.run()
                retry_count += 1
                if retry_count >= 5:
                    logger.error(f"Failed to download file {file_path} after 5 retries.")
                    return False

    logger.info(f"All files for station {num_station} exist. Checking OK")
    return True


"""=====================================================================================================

Agglomération des données météo historiques pour une station : 1 fichier par station

========================================================================================================="""

def aggregate_histo_data(num_station: int):
    station_folder = f"data_meteo_histo/{num_station}"
    station_files = os.listdir(station_folder)
    station_files.sort()
    if len(station_files) == 0:
        raise FileNotFoundError(f"No files found for station {num_station} in folder {station_folder}")

    # Create the output file
    output_file = f"data_meteo_histo/{num_station}/{num_station}_histo.csv"
    with open(output_file, "w") as output:
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

    logger.info(f"Aggregation complete for station {num_station}. File saved to {output_file}")
    return output_file

"""========================================================================================================

Quality check for the aggregated historical data files

=============================================================================================================="""

def check_duplicated_dates(dates: pd.Series, aggregated_file: str) -> bool:
    duplicated_dates = dates[dates.duplicated()]
    if not duplicated_dates.empty:
        logger.error(f"Duplicate dates found in the file {aggregated_file}: {duplicated_dates.tolist()}")
        return False
    logger.info(f"No duplicate dates found in the file {aggregated_file}")
    return True

def check_missing_dates(dates: pd.Series, aggregated_file: str) -> bool:
    dates = pd.to_datetime(dates)
    date_range = pd.date_range(start=dates.min(), end=dates.max())
    missing_dates = date_range[~date_range.isin(dates)]

    if not missing_dates.empty:
        missing_dates = missing_dates.strftime('%Y-%m-%d').tolist()
        logger.error(f"Missing dates found in the file {aggregated_file}: {missing_dates}")
        return False

    logger.info(f"No missing dates found in the file {aggregated_file}")
    return True


def verify_data_quality_in_histo_files(num_station: int):
    station_folder = f"data_meteo_histo/{num_station}"
    aggregated_file = f"{station_folder}/{num_station}_histo.csv"

    if not os.path.isfile(aggregated_file):
        logger.error(f"Aggregated file {aggregated_file} does not exist.")
        return False

    # Read the aggregated file into a DataFrame
    df = pd.read_csv(aggregated_file, sep=';', parse_dates=[1], dayfirst=True)
    dates = df.iloc[:, 1]

    # Check for duplicate dates
    if not check_duplicated_dates(dates, aggregated_file):
        solve_duplicates(dates, aggregated_file)

    # Check for missing dates
    while not check_missing_dates(dates, aggregated_file):
        download_and_add_data_missing_dates(dates, aggregated_file)
        df = pd.read_csv(aggregated_file, sep=';', parse_dates=[1], dayfirst=True)
        dates = df.iloc[:, 1]
        time.sleep(3)

    if check_duplicated_dates(dates, aggregated_file) and check_missing_dates(dates, aggregated_file):
        logger.info(f"Data quality check passed for files {aggregated_file}: No duplicate or missing dates.")
        return True
    else:
        return False

"""======================================================================================================================

Repairing historical data files

==========================================================================================================================="""

def solve_duplicates(dates: pd.Series, aggregated_file: str):
    duplicated_dates = dates[dates.duplicated()]
    if not duplicated_dates.empty:
        logger.info(f"Removing duplicates...")
        df = pd.read_csv(aggregated_file, sep=';', parse_dates=[1], dayfirst=True)
        df.drop_duplicates(subset='DATE', inplace=True)
        df.to_csv(aggregated_file, sep=';', index=False)
        logger.info(f"Duplicates removed from file {aggregated_file}")
    return True


def download_data_date(station_number: int, date_start, date_end):
    downloader = CSVDownloader(
        num_station=station_number,
        date_start=date_start,
        date_end=date_end
    )

    retry_count = 0
    max_retries = 10
    while not downloader.download_is_complete and retry_count < max_retries:
        downloader.run()
        retry_count += 1
        if downloader.download_is_complete:
            logger.info(f"Download successful for station {station_number} from {date_start} to {date_end}")
            return True
        else:
            logger.warning(
                f"Download attempt {retry_count} failed for station {station_number} from {date_start} to {date_end}")

    logger.error(
        f"Failed to download data for station {station_number} from {date_start} to {date_end} after {max_retries} attempts")
    return False

def add_date_to_histo_file(file_paths: list, station_number: int):
    histo_file = from_station_number_to_histo_file_path(station_number)

    if not histo_file:
        raise ValueError("No files provided for aggregation")

    # Read the existing historical file into a DataFrame
    if os.path.exists(histo_file):
        histo_df = pd.read_csv(histo_file, sep=';', parse_dates=[1], dayfirst=True)
    else:
        histo_df = pd.DataFrame()

    # Append the data from all files
    for file_path in file_paths:
        df = pd.read_csv(file_path, sep=';', parse_dates=[1], dayfirst=True)
        df.iloc[:, 1] = df.iloc[:, 1].dt.strftime('%Y-%m-%d')
        df.dropna(how='all', inplace=True)
        histo_df = pd.concat([histo_df, df], ignore_index=True)

        # Remove any empty lines
    histo_df.dropna(how='all', inplace=True)

    # Save the DataFrame back to the CSV file
    histo_df.to_csv(histo_file, sep=';', index=False)

    logger.info(f"Aggregation complete. File saved to {histo_file}")



def download_and_add_data_missing_dates(dates: pd.Series, aggregated_file: str):
    dates = pd.to_datetime(dates)
    date_range = pd.date_range(start=dates.min(), end=dates.max())
    missing_dates = date_range[~date_range.isin(dates)]

    if not missing_dates.empty:
        logger.info(f"Filling missing dates...")
        for date in missing_dates:
            date_iso = convert_date_to_iso(date.strftime('%Y-%m-%d'))
            station_number = from_station_histo_file_name_to_station_number(aggregated_file)

            # Download the missing data
            download_data_date(station_number, date_iso, date_iso)

        # Add the missing data to the aggregated file
        list_file_paths = [from_date_start_end_to_path_name(station_number, date_iso.strftime('%Y-%m-%d'), date_iso.strftime('%Y-%m-%d')) for date_iso in missing_dates]
        add_date_to_histo_file(list_file_paths, station_number)

        logger.info(f"Missing dates files downloaded and added to {aggregated_file}")

    return True

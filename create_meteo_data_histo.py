import os
import pandas as pd

from logs.logging_config import logger
from CSVDownloader import CSVDownloader
from utils import extract_date


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

    # Extract the date column
    dates = df.iloc[:, 1]

    # Check for duplicate dates
    duplicates_check = check_duplicated_dates(dates, aggregated_file)
    solve_duplicates(dates, aggregated_file)

    # Check for missing dates
    missing_dates_check = check_missing_dates(dates, aggregated_file)

    if duplicates_check and missing_dates_check:
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

# def solve_missing_dates(dates: pd.Series, aggregated_file: str):
#     dates = pd.to_datetime(dates)
#     date_range = pd.date_range(start=dates.min(), end=dates.max())
#     missing_dates = date_range[~date_range.isin(dates)]
#
#     if not missing_dates.empty:
#         logger.info(f"Filling missing dates...")
#         df = pd.read_csv(aggregated_file, sep=';', parse_dates=[1], dayfirst=True)
#         for date in missing_dates:
#             convert_date_to_iso(date.strftime('%Y-%m-%d'))
#         df.sort_values(by='DATE', inplace=True)
#         df.to_csv(aggregated_file, sep=';', index=False)
#         logger.info(f"Missing dates filled in file {aggregated_file}")
#     return True
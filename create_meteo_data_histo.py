import pandas as pd
import os
import re

from config import PROJECT_ROOT
from logs.logging_config import logger


def get_existing_station_files(root_directory: str) -> list:
    """
    Generate a list of all station historical data files that exist in the given root directory and its subdirectories.

    :param root_directory: Path to the root directory containing subdirectories with station historical data files.
    :return: List of file paths to station historical data files.
    """
    station_files = []
    pattern = re.compile(r".*_histo\.csv$")

    for subdir, _, files in os.walk(root_directory):
        for file_name in files:
            if pattern.match(file_name):
                file_path = os.path.join(subdir, file_name)
                station_files.append(file_path)

    return station_files


def aggregate_station_files(station_file_paths: list, output_file_path: str) -> bool:
    """
    Aggregate all station historical data files into a single CSV file.

    :param station_file_paths: List of file paths to station historical data files.
    :param output_file_path: Path to the output aggregated CSV file.
    :return: True if aggregation is successful, False otherwise.
    """
    aggregated_df = pd.DataFrame()

    for file_path in station_file_paths:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, sep=";", parse_dates=[1], dayfirst=True)
            aggregated_df = pd.concat([aggregated_df, df], ignore_index=True)
        else:
            logger.error(f"File {file_path} does not exist.")
            return False

    # Remove any empty lines
    aggregated_df.dropna(how="all", inplace=True)

    # Save the aggregated DataFrame to the output CSV file
    aggregated_df.to_csv(output_file_path, sep=";", index=False)
    logger.info(f"Aggregated station data saved to {output_file_path}")

    return True

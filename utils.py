import urllib.parse
import os
from datetime import datetime
from logs.logging_config import logger


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


def ensure_folder_exists(folder_path: str):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.info(f"Folder created: {folder_path}")
    else:
        pass

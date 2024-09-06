import urllib.parse
import os
from datetime import datetime
from logging_config import logger

def extract_date(encoded_date: str) -> str:
    decoded_date = urllib.parse.unquote(encoded_date)
    parsed_date = datetime.strptime(decoded_date, "%Y-%m-%dT%H:%M:%SZ")
    return parsed_date.strftime("%Y-%m-%d")


def ensure_folder_exists(folder_path: str):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.info(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

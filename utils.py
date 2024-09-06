import urllib.parse
from datetime import datetime


def extract_date(encoded_date: str) -> str:
    decoded_date = urllib.parse.unquote(encoded_date)
    parsed_date = datetime.strptime(decoded_date, "%Y-%m-%dT%H:%M:%SZ")
    return parsed_date.strftime("%Y-%m-%d")
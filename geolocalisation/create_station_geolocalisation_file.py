import csv
import os
import requests
import json
from typing import List, Dict, Any

from config import BASE_URL, API_KEY
from logs.logging_config import logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


@retry(
    stop=stop_after_attempt(10),
    wait=wait_exponential(
        multiplier=1, min=2, max=60
    ),  # Exponential backoff (2, 4, 8, ... max 60 seconds)
    retry=retry_if_exception_type(
        requests.exceptions.RequestException
    ),  # Retry for request exceptions
)
def get_json_info_stations_departement(num_departement: int) -> bytes:
    """
    Get the JSON output from the API for a specific departement.
    Get information of stations of a specific departement.
    Contains station ids, longitude, latitude, altitude, name, etc.
    :rtype: object
    :param num_departement: The number of the departement.
    :return: JSON response content as bytes.
    """
    url = (
        f"{BASE_URL}/public/DPClim/v1/"
        f"liste-stations/quotidienne?"
        f"id-departement={num_departement}"
    )

    headers = {"accept": "*/*", "Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        logger.info(
            f"Successfully retrieved info of stations for departement {num_departement}"
        )
        return response.content
    else:
        logger.error(
            f"Failed to retrieve info of stations for departement {num_departement}"
        )
        response.raise_for_status()


def load_json_from_bytes(json_bytes: bytes) -> List[Dict[str, Any]]:
    """
    Load JSON data from bytes.
    :param json_bytes: JSON data in bytes.
    :return: Parsed JSON data as a list of dictionaries.
    """
    json_output = json_bytes.decode("utf-8")
    return json.loads(json_output)


def get_list_stations_in_a_departement(num_departement: int) -> List[int]:
    """
    Get the list of station IDs from a departement.
    The json input contains all information about the stations.
    :param num_departement: The number of the departement.
    :return: List of station IDs.
    """
    try:
        info_stations_per_departement = get_json_info_stations_departement(
            num_departement
        )
        stations_data = load_json_from_bytes(info_stations_per_departement)
        return [station["id"] for station in stations_data]
    except KeyError as e:
        logger.error(f"Key error: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to get the list of station IDs: {e}")
        raise


def write_station_data_to_csv(stations_data: List[Dict[str, Any]], csv_file: str):
    """
    Write station data to a CSV file.
    :param stations_data: List of dictionaries containing station data.
    :param csv_file: The name of the CSV file to create or update.
    """
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["id_station", "name", "longitude", "latitude", "altitude"])

        for station in stations_data:
            writer.writerow(
                [
                    station["id"],
                    station["nom"],
                    station["lon"],
                    station["lat"],
                    station["alt"],
                ]
            )


def create_or_update_csv_with_departement_stations_info(
    num_departement: int, csv_file: str = "data/stations.csv"
):
    """
    Create or update a CSV file with stations information from a specific departement.
    Stations info are : id, name, latitude, longitude, altitude.
    :param num_departement: The number of the departement.
    :param csv_file: The name of the CSV file to create or update.
    """
    try:
        info_stations_per_departement = get_json_info_stations_departement(
            num_departement
        )
        stations_data = load_json_from_bytes(info_stations_per_departement)
        write_station_data_to_csv(stations_data, csv_file)
        logger.info(
            f"Successfully updated {csv_file} with departement {num_departement}"
        )
    except Exception as e:
        logger.error(
            f"Failed to update {csv_file} with departement {num_departement}. Error: {e}"
        )
        raise e

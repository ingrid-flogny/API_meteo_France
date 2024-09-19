import csv
import os
import requests
import json

from config import BASE_URL, API_KEY
from logs.logging_config import logger


def get_json_info_stations_departement(num_departement: int) -> bytes:
    """
    Get the JSON output from the API for a specific departement.
    Get information of stations of a specific departement.
    Contains station ids, longitude, latitude, altitude, name, etc.
    :return:
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


def load_json_from_bytes(json_bytes: bytes) -> json:
    json_output = json_bytes.decode("utf-8")
    json_output = json.loads(json_output)
    return json_output


def get_list_stations_in_a_departement(num_departement: int) -> list:
    """
    Get the list of station IDs from a departement.
    The json input contains all information about the stations.
    :param api_output_json: JSON output from the API.
    :return: List of station IDs.
    """
    try:
        # Get the stations information per departement
        info_stations_per_departement = get_json_info_stations_departement(
            num_departement
        )
        info_stations_per_departement = load_json_from_bytes(
            info_stations_per_departement
        )

        station_ids = [station["id"] for station in info_stations_per_departement]
        return station_ids
    except KeyError as e:
        logger.error(f"Key error: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to get the list of station IDs: {e}")
        raise


def create_or_update_csv_with_departement_stations_info(
    num_departement: int, csv_file="data/stations.csv"
):
    """
    Create or update a CSV file with stations information from a specific departement.
    Stations info are : id, name, latitude, longitude, altitude.

    :param station: Station object containing the station information.
    :param csv_file: The name of the CSV file to create or update.
    """
    try:
        file_exists = os.path.isfile(csv_file)

        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)

            # Write the header if the file does not exist
            if not file_exists:
                writer.writerow(
                    ["id_station", "name", "longitude", "latitude", "altitude"]
                )

            # Get the stations information per departement
            info_stations_per_departement = get_json_info_stations_departement(
                num_departement
            )
            info_stations_per_departement = load_json_from_bytes(
                info_stations_per_departement
            )

            # Write the station data
            for station in info_stations_per_departement:
                writer.writerow(
                    [
                        station["id"],
                        station["nom"],
                        station["lon"],
                        station["lat"],
                        station["alt"],
                    ]
                )

        logger.info(
            f"Successfully updated {csv_file} with departement {num_departement}"
        )

    except Exception as e:
        logger.error(
            f"Failed to update {csv_file} with departement {num_departement}. "
            f"Station concerned :{station['id']}"
            f"Error : {e}"
        )
        raise

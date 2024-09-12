import csv
import os
from logs.logging_config import logger


def create_or_update_csv(station, csv_file="data/stations.csv"):
    """
    Create or update a CSV file with station information.

    :param station: Station object containing the station information.
    :param csv_file: The name of the CSV file to create or update.
    """
    try:
        file_exists = os.path.isfile(csv_file)

        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)

            # Write the header if the file does not exist
            if not file_exists:
                writer.writerow(["id_station", "longitude", "latitude", "altitude"])

            # Write the station data
            writer.writerow(
                [
                    station.num_station,
                    station.longitude,
                    station.latitude,
                    station.altitude,
                ]
            )

        logger.info(
            f"Successfully updated {csv_file} with station {station.num_station}"
        )

    except Exception as e:
        logger.error(
            f"Failed to update {csv_file} with station {station.num_station}: {e}"
        )
        raise

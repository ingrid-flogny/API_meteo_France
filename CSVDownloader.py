import json
import requests
import time
import os
from config import API_KEY, BASE_URL
from utils import extract_date, ensure_folder_exists
from logs.logging_config import logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


class CSVDownloader:
    """
    Class to download the CSV file for a given station and date range.
    CSV file contains weather data for a station for a given date range.
    Date range must be 1 year maximum.
    """

    def __init__(self, num_station: str, date_start: str, date_end: str):
        """

        :param num_station: Station number
        :param date_start: Date range start. Date ISO format.
        :param date_end: Date range end. Date ISO format.
        """
        self.base_url = BASE_URL
        self.api_key = API_KEY
        self.num_station = num_station
        self.date_start = date_start
        self.date_end = date_end
        self.download_is_complete = False
        self.save_path = (
            f"data_meteo_histo/{num_station}/from{extract_date(date_start)}_"
            f"to{extract_date(date_end)}.csv"
        )
        self.headers = {"accept": "*/*", "Authorization": f"Bearer {self.api_key}"}

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_exponential(
            multiplier=1, min=2, max=60
        ),  # Exponential backoff (2, 4, 8, ... max 60 seconds)
        retry=retry_if_exception_type(
            requests.exceptions.RequestException
        ),  # Retry for request exceptions
    )
    def get_command_number(self):
        """
        Get the command number for the given station and date range.
        This command number will be used to download the CSV file.
        :return:
        """
        url = (
            f"{self.base_url}/public/DPClim/v1/commande-station/quotidienne?"
            f"id-station={self.num_station}&date-deb-periode={self.date_start}&"
            f"date-fin-periode={self.date_end}"
        )
        response = requests.get(url, headers=self.headers)
        logger.info(f"Response Status Code:{response.status_code}")

        if response.status_code == 202:
            logger.info(
                f"Request accepted for station {self.num_station} from "
                f"{self.date_start} to {self.date_end}"
            )
            return response.content
        else:
            logger.error(f"Response Content: {response.content}")
            response.raise_for_status()

    def extract_command_number(self, api_response):
        """
        Extract the command number from the API response
        :param api_response:
        :return:
        """
        response_str = api_response.decode("utf-8")
        response_dict = json.loads(response_str)
        return response_dict["elaboreProduitAvecDemandeResponse"]["return"]

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_exponential(
            multiplier=1, min=2, max=60
        ),  # Exponential backoff (2, 4, 8, ... max 60 seconds)
        retry=retry_if_exception_type(
            requests.exceptions.RequestException
        ),  # Retry for request exceptions
    )
    def download_csv(self, command_number: int):
        """
        Download the CSV file for the given command number
        :param command_number:
        :return:
        """
        url = (
            f"{self.base_url}/public/DPClim/v1/commande/fichier?"
            f"id-cmde={command_number}"
        )

        while True:
            response = requests.get(url, headers=self.headers)
            logger.info(f"Response Status Code:{response.status_code}")

            if response.status_code == 204:
                logger.info("Production encore en attente ou en cours.")
                time.sleep(5)

            elif response.status_code == 201:
                logger.info("Downloading file...")
                station_folder = f"data_meteo_histo/{self.num_station}"
                ensure_folder_exists(station_folder)

                # Save the file to the station folder if it doesn't exist
                if not os.path.exists(self.save_path):
                    with open(self.save_path, "wb") as file:
                        file.write(response.content)
                    logger.info(
                        f"File downloaded successfully and saved to {self.save_path}"
                    )
                else:
                    logger.info(f"File already exists at {self.save_path}")
                self.download_is_complete = True
                return response.content

            else:
                logger.error(f"Response Content: {response.content}")
                response.raise_for_status()

    def run(self):
        """
        Run the downloader.
        :return:
        """
        try:
            command_number = self.extract_command_number(self.get_command_number())
            self.download_csv(command_number)
        except requests.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred: {err}")

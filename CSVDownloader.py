import json
import requests
import time
from config import API_KEY, BASE_URL
from utils import extract_date, ensure_folder_exists
from logging_config import logger


class CSVDownloader:
    def __init__(self, num_station, date_start, date_end):
        self.base_url = BASE_URL
        self.num_station = num_station
        self.date_start = date_start
        self.date_end = date_end
        self.api_key = API_KEY
        self.save_path = f"data_meteo_histo/{num_station}/from{extract_date(date_start)}_to{extract_date(date_end)}.csv"
        self.headers = {
            "accept": "*/*",
            "Authorization": f"Bearer {self.api_key}"
        }

    def get_command_number(self):
        url = f"{self.base_url}/public/DPClim/v1/commande-station/quotidienne?id-station={self.num_station}&date-deb-periode={self.date_start}&date-fin-periode={self.date_end}"
        response = requests.get(url, headers=self.headers)
        logger.info(f"Response Status Code:{response.status_code}")

        if response.status_code == 202:
            return response.content
        else:
            logger.error(f"Response Content: {response.content}")
            response.raise_for_status()

    def extract_command_number(self, api_response):
        response_str = api_response.decode("utf-8")
        response_dict = json.loads(response_str)
        return response_dict["elaboreProduitAvecDemandeResponse"]["return"]

    def download_csv(self, command_number):
        url = f"{self.base_url}/public/DPClim/v1/commande/fichier?id-cmde={command_number}"

        while True:
            response = requests.get(url, headers=self.headers)
            logger.info(f"Response Status Code:{response.status_code}")

            if response.status_code == 204:
                logger.info("Production encore en attente ou en cours.")
                time.sleep(5)

            elif response.status_code == 201:
                station_folder = f"data_meteo_histo/{self.num_station}"
                ensure_folder_exists(station_folder)

                # Save the file to the station folder
                with open(self.save_path, "wb") as file:
                    file.write(response.content)
                logger.info(f"File downloaded successfully and saved to {self.save_path}")
                return response.content

            else:
                logger.error(f"Response Content: {response.content}")
                response.raise_for_status()

    def run(self):
        try:
            command_number = self.extract_command_number(self.get_command_number())
            self.download_csv(command_number)
        except requests.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred: {err}")

if __name__ == '__main__':
    downloader = CSVDownloader(
        num_station=59343001,
        date_start="2024-08-01T00%3A00%3A00Z",
        date_end="2024-09-05T00%3A00%3A00Z"
    )
    downloader.run()
import json
import requests
import time
from config import API_KEY, BASE_URL
from utils import extract_date


class CSVDownloader:
    def __init__(self, num_station, date_start, date_end):
        self.base_url = BASE_URL
        self.num_station = num_station
        self.date_start = date_start
        self.date_end = date_end
        self.api_key = API_KEY
        self.save_path = f"data_meteo_histo/{num_station}_from{extract_date(date_start)}_to{extract_date(date_end)}.csv"
        self.headers = {
            "accept": "*/*",
            "Authorization": f"Bearer {self.api_key}"
        }

    def get_command_number(self):
        url = f"{self.base_url}/public/DPClim/v1/commande-station/quotidienne?id-station={self.num_station}&date-deb-periode={self.date_start}&date-fin-periode={self.date_end}"
        response = requests.get(url, headers=self.headers)
        print("Response Status Code:", response.status_code)

        if response.status_code == 202:
            return response.content
        else:
            print("Response Content:", response.content)
            response.raise_for_status()

    def extract_command_number(self, api_response):
        response_str = api_response.decode("utf-8")
        response_dict = json.loads(response_str)
        return response_dict["elaboreProduitAvecDemandeResponse"]["return"]

    def download_csv(self, command_number):
        url = f"{self.base_url}/public/DPClim/v1/commande/fichier?id-cmde={command_number}"
        while True:
            response = requests.get(url, headers=self.headers)
            print("Response Status Code:", response.status_code)
            if response.status_code == 204:
                print("Production encore en attente ou en cours.")
                time.sleep(5)
            elif response.status_code == 201:
                with open(self.save_path, "wb") as file:
                    file.write(response.content)
                print(f"File downloaded successfully and saved to {self.save_path}")
                return response.content
            else:
                print("Response Content:", response.content)
                response.raise_for_status()

    def run(self):
        try:
            command_number = self.extract_command_number(self.get_command_number())
            self.download_csv(command_number)
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

if __name__ == '__main__':
    downloader = CSVDownloader(
        num_station=59343001,
        date_start="2024-08-01T00%3A00%3A00Z",
        date_end="2024-09-05T00%3A00%3A00Z"
    )
    downloader.run()
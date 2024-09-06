import json
import requests
import time
from config import API_KEY

base_url = "https://public-api.meteofrance.fr"
num_station = 59343001
date_start = "2024-08-01T00%3A00%3A00Z"
date_end = "2024-09-06T00%3A00%3A00Z"
save_path = "data_meteo.csv"

def get_data(url: str, headers):
    response = requests.get(url, headers=headers)
    print("Response Status Code:", response.status_code)
    if response.status_code == 202:
        return response.content
    else:
        print("Response Content:", response.content)
        response.raise_for_status()

def extract_command_number(api_response: bytes) -> int:
    response_str = api_response.decode("utf-8")
    response_dict = json.loads(response_str)
    return response_dict["elaboreProduitAvecDemandeResponse"]["return"]

def download_csv(command_number: int, headers):
    url = f"{base_url}/public/DPClim/v1/commande/fichier?id-cmde={command_number}"
    while True:
        response = requests.get(url, headers=headers)
        print("Response Status Code:", response.status_code)
        if response.status_code == 204:
            print("Production encore en attente ou en cours.")
            time.sleep(10)
        elif response.status_code == 201:
            with open(save_path, "wb") as file:
                file.write(response.content)
            print(f"File downloaded successfully and saved to {save_path}")
            print("Response Content:", response.content)
            return response.content
        else:
            print("Response Content:", response.content)
            response.raise_for_status()

if __name__ == '__main__':
    url = f"{base_url}/public/DPClim/v1/commande-station/quotidienne?id-station={num_station}&date-deb-periode={date_start}&date-fin-periode={date_end}"

    if not API_KEY:
        raise ValueError("API_KEY is missing or empty in config.py")

    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        command_number = extract_command_number(get_data(url, headers))
        print(command_number)
        download_csv(command_number, headers)

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
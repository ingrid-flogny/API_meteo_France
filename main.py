import json
import requests
import time

from config import API_KEY

base_url = "https://public-api.meteofrance.fr"

# PARAMETRAGE
num_station = 59343001
date_start = "2024-01-08T00%3A00%3A00Z"
date_end = "2024-08-11T00%3A00%3A00Z"

def get_data(url: str, headers: json):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


if __name__ == '__main__':

    url = f"{base_url}/public/DPClim/v1/commande-station/quotidienne?id-station={num_station}&date-deb-periode={date_start}&date-fin-periode={date_end}"
    print("url", url)

    headers = {
        "apikey": API_KEY,
        "accept": "*/*"
    }

    try:
        data = get_data(url, headers)
        print(data)
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")



import json
import requests
from config import API_KEY

base_url = "https://public-api.meteofrance.fr"
num_station = 59343001
date_start = "2024-08-01T00%3A00%3A00Z"
date_end = "2024-09-03T00%3A00%3A00Z"


def get_data(url: str, headers):
    response = requests.get(url, headers=headers)
    print("Response Status Code:", response.status_code)
    if response.status_code == 200:
        return response.json()
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
        data = get_data(url, headers)
        print(data)
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

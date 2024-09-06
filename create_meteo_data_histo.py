import os
from logs.logging_config import logger
from CSVDownloader import CSVDownloader

date_start_end= {
    "2017-01-01T00%3A00%3A00Z": "2018-01-01T00%3A00%3A00Z",
    "2018-01-01T00%3A00%3A00Z": "2019-01-01T00%3A00%3A00Z",
    "2019-01-01T00%3A00%3A00Z": "2020-01-01T00%3A00%3A00Z",
    "2020-01-01T00%3A00%3A00Z": "2021-01-01T00%3A00%3A00Z",
    "2021-01-01T00%3A00%3A00Z": "2022-01-01T00%3A00%3A00Z",
    "2022-01-01T00%3A00%3A00Z": "2023-01-01T00%3A00%3A00Z",
    "2023-01-01T00%3A00%3A00Z": "2024-01-01T00%3A00%3A00Z",
    "2024-01-01T00%3A00%3A00Z": "2024-09-05T00%3A00%3A00Z",
}

def download_histo_per_station(num_station: int):
    for date_start, date_end in date_start_end.items():
        downloader = CSVDownloader(
            num_station=num_station,
            date_start=date_start,
            date_end=date_end
        )
        downloader.run()

def verify_files_histo_all_exist(num_station: int):
    for date_start, date_end in date_start_end.items():
        file_path = (
            f"data_meteo_histo/{num_station}/from{date_start}_"
            f"to{date_end}.csv"
        )
        if not os.path.exists(file_path):
            logger.info(f"File {file_path} does not exist.")
            downloader = CSVDownloader(
                num_station=num_station,
                date_start=date_start,
                date_end=date_end
            )
            downloader.run()
            return False
    return True
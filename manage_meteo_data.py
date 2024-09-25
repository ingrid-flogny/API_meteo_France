from utils import rename_columns_using_mapping
from logs.logging_config import logger


def rename_columns_stations_histo_file() -> bool:
    """
    Rename the columns in the historical data file for a station.
    :return:
    """
    description_file_path = f"data/description_variables_meteo.csv"
    histo_file_path = f"data_meteo_histo/stations_weather_data_histo.csv"
    rename_columns_using_mapping(description_file_path, histo_file_path)

    logger.info(f"Columns renamed in the stations weather data historical file.")

    return True

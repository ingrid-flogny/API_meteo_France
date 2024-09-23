from utils import rename_columns_using_mapping
from logs.logging_config import logger


def rename_columns_station_histo_file(station_number: int) -> bool:
    """
    Rename the columns in the historical data file for a station.
    :param station_number: Weather station number
    :return:
    """
    description_file_path = f"data/description_variables_meteo.csv"
    histo_file_path = f"data_meteo_histo/{station_number}/{station_number}_histo.csv"
    rename_columns_using_mapping(description_file_path, histo_file_path)

    logger.info(
        f"Columns renamed in the historical data file for station {station_number}."
    )

    return True

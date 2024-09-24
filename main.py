from config import PROJECT_ROOT
from create_meteo_data_histo import get_existing_station_files, aggregate_station_files
from create_station_meteo_data_histo import (
    download_histo_per_station,
    verify_files_histo_all_exist,
    aggregate_histo_data,
    verify_data_quality_in_histo_files,
    delete_yearly_files,
)
from manage_meteo_data import rename_columns_station_histo_file

"""=====================================================================================================
    Create weather histo file of a given station
===================================================================================================="""

# # Lille Lesquin station: 59343001
# # Download all historical data for a station
# download_histo_per_station(13054001)
# verify_files_histo_all_exist(13054001)
#
# # Aggregate all historical data for a station
# aggregate_histo_data(13054001)
# verify_data_quality_in_histo_files(13054001)
#
# # Rename the file
# rename_columns_station_histo_file(13054001)

delete_yearly_files(13054001)

"""=====================================================================================================
    Aggregate weather histo files of all stations
===================================================================================================="""

# root_directory = PROJECT_ROOT + "/data_meteo_histo/"
# output_file = "data_meteo_histo/stations_weather_data_histo.csv"
#
# station_files = get_existing_station_files(root_directory)
# aggregate_station_files(station_files, output_file)

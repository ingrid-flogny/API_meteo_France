from config import PROJECT_ROOT
from create_meteo_data_histo import get_existing_station_files, aggregate_station_files
from create_station_meteo_data_histo import (
    download_histo_per_station,
    verify_files_histo_all_exist,
    aggregate_histo_data,
    verify_data_quality_in_histo_files,
    delete_yearly_files,
)
from manage_meteo_data import rename_columns_stations_histo_file
from utils import filter_columns_histo_file

"""=====================================================================================================
    Create weather histo file of a given station
===================================================================================================="""

# Lille Lesquin station: 59343001

# num_station = '94042001'
# # Download all historical data for a station
# download_histo_per_station(num_station)
# verify_files_histo_all_exist(num_station)
#
# # Aggregate all historical data for a station
# aggregate_histo_data(num_station)
# verify_data_quality_in_histo_files(num_station)
#
# # Finish
# delete_yearly_files(num_station)

"""=====================================================================================================
    Create full histo file : Aggregate weather histo files of all stations
===================================================================================================="""

# root_directory = PROJECT_ROOT + "/data_meteo_histo/"
# output_file = PROJECT_ROOT + "/data_meteo_histo/stations_weather_data_histo.csv"
#
# station_files = get_existing_station_files(root_directory)
# aggregate_station_files(station_files, output_file)
# rename_columns_stations_histo_file()


"""=====================================================================================================
    Filter columns of histo file
===================================================================================================="""

columns_to_keep_in_histo_file = [
    "POSTE",
    "DATE",
    "HAUTEUR DE PRECIPITATIONS QUOTIDIENNE",
    "DUREE DES PRECIPITATIONS QUOTIDIENNES",
    "TEMPERATURE MINIMALE SOUS ABRI QUOTIDIENNE",
    "TEMPERATURE MAXIMALE SOUS ABRI QUOTIDIENNE",
    "TEMPERATURE MOYENNE SOUS ABRI QUOTIDIENNE",
    "DUREE DE GEL QUOTIDIENNE",
    "MOYENNE DES VITESSES DU VENT A 10M QUOTIDIENNE",
    "VITESSE VENT MAXI INSTANTANE QUOTIDIENNE",
    "HUMIDITE RELATIVE MINIMALE QUOTIDIENNE",
    "HUMIDITE RELATIVE MAXIMALE QUOTIDIENNE",
    "DUREE HUMIDITE <= 40% QUOTIDIENNE",
    "DUREE HUMIDITE >= 80% QUOTIDIENNE",
    "HUMIDITE RELATIVE MOYENNE",
    "RAYONNEMENT GLOBAL QUOTIDIEN",
    "MAX DES INDICES UV HORAIRE",
    "OCCURRENCE DE NEIGE QUOTIDIENNE",
    "OCCURRENCE DE BROUILLARD QUOTIDIENNE",
    "OCCURRENCE D'ORAGE QUOTIDIENNE",
    "OCCURRENCE DE GRELE QUOTIDIENNE",
    "OCCURRENCE DE VERGLAS",
    "OCCURRENCE DE FUMEE QUOTIDIENNE",
    "OCCURRENCE DE BRUME QUOTIDIENNE",
    "OCCURRENCE ECLAIR QUOTIDIENNE",
    "ETP CALCULEE AU POINT DE GRILLE LE PLUS PROCHE",
    "HAUTEUR DE NEIGE TOMBEE EN 24H",
]

input_histo_file = PROJECT_ROOT + "/data_meteo_histo/stations_weather_data_histo.csv"
output_histo_file = (
    PROJECT_ROOT + "/data_meteo_histo/stations_weather_data_histo_filtered.csv"
)


filter_columns_histo_file(
    input_histo_file, output_histo_file, columns_to_keep_in_histo_file
)

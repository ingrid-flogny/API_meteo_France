from geolocalisation.create_station_geolocalisation_file import (
    create_or_update_csv_with_departement_stations_info,
)

list_departements_francais = list(range(1, 96)) + [
    971,
    972,
    973,
    974,
    975,
    984,
    986,
    987,
    988,
]
list_all_departements = []

for num_departement in list_departements_francais:
    create_or_update_csv_with_departement_stations_info(num_departement)

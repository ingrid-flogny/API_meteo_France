from create_meteo_data_histo import (
    download_histo_per_station,
    verify_files_histo_all_exist,
    aggregate_histo_data,
    verify_data_quality_in_histo_files,
)

# Download all historical data for a station
download_histo_per_station(59343001)
verify_files_histo_all_exist(59343001)

# Aggregate all historical data for a station
aggregate_histo_data(59343001)
verify_data_quality_in_histo_files(59343001)

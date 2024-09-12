import requests
import json

from config import API_KEY, BASE_URL
from geolocalisation.utils_geolocalisation import (
    from_station_info_to_name,
    from_station_info_to_latitude,
    from_station_info_to_longitude,
    from_station_info_to_altitude,
    from_station_info_to_lieuDit,
    from_station_info_to_bassin,
)
from logs.logging_config import logger


class Station:
    def __init__(self, num_station: int):
        """
        Initialize a Station object.

        :param num_station: The station number.
        """
        self.num_station = num_station
        self.station_info: json = None

        self.name: str = None
        self.lieuDit: str = None
        self.bassin: str = None

        self.longitude: float = None
        self.latitude: float = None
        self.altitude: float = None

    def __repr__(self):
        """
        Return a string representation of the Station object.
        """
        return (
            f"Station(num_station={self.num_station}, "
            f"name={self.name}, "
            f"lieuDit={self.lieuDit}, "
            f"bassin={self.bassin}, "
            f"latitude={self.latitude}, "
            f"longitude={self.longitude}, "
            f"altitude={self.altitude})"
        )

    def get_station_info(self) -> json:
        """
        Get the station information.
        """
        url = (
            f"{BASE_URL}/public/DPClim/v1/"
            f"information-station?"
            f"id-station={self.num_station}"
        )

        headers = {"accept": "*/*", "Authorization": f"Bearer {API_KEY}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            logger.info(
                f"Request accepted for getting information of "
                f"station {self.num_station}"
            )
            station_info = response.content
            self.station_info = json.loads(station_info)
            return station_info
        else:
            logger.error(f"Response Content: {response.content}")
            response.raise_for_status()

    def fill_station_info(self) -> str:
        """
        Fill the station information.
        """
        self.name = from_station_info_to_name(self.station_info)
        self.lieuDit = from_station_info_to_lieuDit(self.station_info)
        self.bassin = from_station_info_to_bassin(self.station_info)

        self.latitude = from_station_info_to_latitude(self.station_info)
        self.longitude = from_station_info_to_longitude(self.station_info)
        self.altitude = from_station_info_to_altitude(self.station_info)

        pass

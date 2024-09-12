import json


def from_station_info_to_name(station_info: dict) -> str:
    """
    Get the name of a station from its information.
    :param station_info:
    :return:
    """
    return station_info[0]["nom"]


def from_station_info_to_lieuDit(station_info: dict) -> str:
    """
    Get the lieuDit of a station from its information.
    :param station_info:
    :return:
    """
    return station_info[0]["lieuDit"]


def from_station_info_to_bassin(station_info: dict) -> str:
    """
    Get the bassin of a station from its information.
    :param station_info:
    :return:
    """
    return station_info[0]["bassin"]


def from_station_info_to_longitude(station_info: dict) -> float:
    """
    Get the longitude of a station from its information.
    :param station_info:
    :return:
    """
    return station_info[0]["positions"][-1]["longitude"]


def from_station_info_to_latitude(station_info: dict) -> float:
    """
    Get the latitude of a station from its information.
    :param station_info:
    :return:
    """
    return station_info[0]["positions"][-1]["latitude"]


def from_station_info_to_altitude(station_info: dict) -> float:
    """
    Get the altitude of a station from its information.
    :param station_info:
    :return:
    """
    return station_info[0]["positions"][-1]["altitude"]

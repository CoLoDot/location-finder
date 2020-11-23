#! /usr/bin/env python
from geopy.geocoders import Nominatim
from .constants import LOCATE_STOP_WORDS


def locate(city: str) -> dict:
    geolocator = Nominatim(user_agent="locator")
    coordonates = {
        "location": "",
        "lat": "",
        "long": "",
        "country": ""
    }
    location = geolocator.geocode(city, addressdetails=True)
    if location:
        country = geolocator.reverse(
            [location.latitude, location.longitude], language='fr')
        coordonates['location'] = str(location)
        coordonates['lat'] = str(location.latitude)
        coordonates["long"] = str(location.longitude)
        try:
            coordonates["country"] = country.raw['address']['country']
        except KeyError:
            pass
    else:
        _city = city.split()
        city_query = [i for i in _city if not i in LOCATE_STOP_WORDS]
        for query_item in city_query:
            _location = geolocator.geocode(query_item, addressdetails=True)
            if _location:
                _country = geolocator.reverse(
                    [_location.latitude, _location.longitude], language='fr')
                coordonates['location'] = str(_location)
                coordonates['lat'] = str(_location.latitude)
                coordonates["long"] = str(_location.longitude)
                try:
                    coordonates["country"] = _country.raw['address']['country']
                except KeyError:
                    pass
                break

    return coordonates

#! /usr/bin/env python
import time
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
    try:
        time.sleep(1)
        location = geolocator.geocode(city, addressdetails=True)
        if location:
            time.sleep(1)
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
            time.sleep(1)
            _city = city.split()
            city_query = [i for i in _city if not i in LOCATE_STOP_WORDS]
            for query_item in city_query:
                time.sleep(1)
                _location = geolocator.geocode(query_item, addressdetails=True)
                if _location:
                    time.sleep(1)
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
    except:
        pass

    return coordonates

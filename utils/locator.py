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
        location = geolocator.geocode(
            city.strip(), timeout=2, addressdetails=True, language='fr')
        if location:
            try:
                coordonates['location'] = str(location)
            except KeyError:
                pass
            try:
                coordonates['lat'] = str(location.latitude)
            except KeyError:
                pass
            try:
                coordonates["long"] = str(location.longitude)
            except KeyError:
                pass
            try:
                coordonates["country"] = location.raw['address']['country']
            except KeyError:
                pass
        else:
            _city = city.split()
            city_query = [
                i for i in _city if not i in LOCATE_STOP_WORDS]
            for query_item in city_query:
                time.sleep(1)
                _location = geolocator.geocode(
                    query_item, timeout=2, addressdetails=True, language='fr')
                if _location:
                    try:
                        coordonates['location'] = str(_location)
                    except KeyError:
                        pass
                    try:
                        coordonates['lat'] = str(_location.latitude)
                    except KeyError:
                        pass
                    try:
                        coordonates["long"] = str(_location.longitude)
                    except KeyError:
                        pass
                    try:
                        coordonates["country"] = _location.raw['address']['country']
                    except KeyError:
                        pass
                    break
    except:
        print('Exception raised : unknown')
        pass

    return coordonates

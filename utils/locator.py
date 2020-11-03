#! /usr/bin/env python
from geopy.geocoders import Nominatim


def locate(entities: list) -> list:
    cities_found = entities
    coordonates = []
    geolocator = Nominatim(user_agent="locator")

    for city in cities_found:
        location = geolocator.geocode(city)
        if location:
            coordonates.append({
                "location": city,
                "lat": location.latitude,
                "long": location.longitude
            })
    return coordonates

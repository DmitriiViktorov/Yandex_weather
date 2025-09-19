from geopy import Nominatim

geolocator = Nominatim(user_agent="yandex_weather_parser")


def city_coordinate(city: str) -> list[dict[str, str]]:
    full_city_name = f"{city}, Россия"

    if locations := geolocator.geocode(full_city_name, exactly_one=False):
        return [
            {
                "address": location.address,
                "lat": location.latitude,
                "lon": location.longitude,
            }
            for location in locations
        ]
    return []
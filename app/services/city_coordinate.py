from geopy import Nominatim

geolocator = Nominatim(user_agent="yandex_weather_parser")


def city_coordinate(city: str) -> list[dict[str, str]]:
    """Определяет возможные города на основании запроса пользователя, возвращает список городов с координатами"""
    if locations := geolocator.geocode(city, exactly_one=False):
        return [
            {
                "address": location.address,
                "lat": location.latitude,
                "lon": location.longitude,
            }
            for location in locations
        ]
    return []
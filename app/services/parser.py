from bs4 import BeautifulSoup

class WeatherParser:
    """
    Парсер данных о погоде в выбранном городе с использованием информации с сервиса Яндекс Погода.

    """
    def __init__(self, city: str):
        self.city = city

    def _city_weather_url(self):
        ...
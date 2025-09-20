import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


DAYS_LENGTH = 7


class WeatherParser:
    """
    Парсер данных о погоде с сервиса Яндекс.Погода.
    Отвечает только за извлечение и первичную обработку HTML данных.
    """

    def __init__(self, address: str, latitude: float, longitude: float):
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def _city_weather_url(self) -> str:
        """Формирует URL для запроса погоды по координатам."""
        base_url = "https://yandex.ru/pogoda/ru?"
        coordinates = f"lat={self.latitude}&lon={self.longitude}"
        return base_url + coordinates

    def _parse_temp(self, temp_str: str) -> int | None:
        """
        Преобразует строку температуры из Яндекс.Погоды в целое число.
        Примеры:
            "+12°" -> 12
            "-5°" -> -5
            "0°" -> 0
        """
        if not temp_str:
            return None
        temp_str = temp_str.strip().replace("°", "")
        try:
            return int(temp_str)
        except ValueError:
            return None

    def _extract_magnetic_field(self, soup: BeautifulSoup) -> str | None:
        """Извлекает информацию о магнитном поле."""
        container = soup.select_one("div[class^='AppForecastDayDuration_info']")
        if not container:
            return None

        for item in container.select("div[class^='AppForecastDayDuration_item']"):
            caption = item.select_one("div[class^='AppForecastDayDuration_caption']")
            value = item.select_one("div[class^='AppForecastDayDuration_value']")
            if caption and caption.get_text(strip=True) == "Магнитное поле":
                return value.get_text(strip=True) if value else None
        return None

    def parse_raw_weather_data(self) -> dict:
        """
        Парсит данные о погоде с сайта и возвращает структурированные данные.
        """
        weather_url = self._city_weather_url()
        html_page = requests.get(weather_url)

        soup = BeautifulSoup(html_page.content, "html.parser")
        weather_data = soup.select("article[class^='AppForecastDay']")[:DAYS_LENGTH]

        day_parts = {"m": "Утро", "d": "День", "e": "Вечер", "n": "Ночь"}

        result = {}
        today = datetime.today().date()

        for i, day_info in enumerate(weather_data):
            date = str(today + timedelta(days=i))

            result[date] = {"periods_info": {}}

            for part in day_parts.keys():
                temp = day_info.find("div", style=lambda s: s and f"grid-area:{part}-temp" in s)
                text = day_info.find("div", style=lambda s: s and f"grid-area:{part}-text" in s)
                hum = day_info.find("div", style=lambda s: s and f"grid-area:{part}-hum" in s)
                press = day_info.find("div", style=lambda s: s and f"grid-area:{part}-press" in s)

                temp_int = self._parse_temp(temp.get_text(strip=True) if temp else None)

                result[date]["periods_info"][day_parts[part]] = {
                    "temp": temp_int,
                    "text": text.get_text(strip=True) if text else None,
                    "humidity": hum.get_text(strip=True) if hum else None,
                    "pressure": int(press.get_text(strip=True)) if press and press.get_text(
                        strip=True).isdigit() else None,
                }

        mag_field = self._extract_magnetic_field(soup)

        for date in result:
            result[date]["mag_field"] = mag_field

        return result

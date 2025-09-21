from app.core.conf import settings


class WeatherAnalyzer:
    """
    Анализатор данных о погоде.
    Отвечает за обработку, расчеты и формирование итоговых данных.
    """

    def _calculate_average_temp(self, periods_info: dict) -> float | None:
        """Вычисляет среднюю температуру за световой день."""
        day_periods = ["Утро", "День", "Вечер"]
        temps = [
            periods_info[p]["temp"]
            for p in day_periods
            if periods_info.get(p) and periods_info[p]["temp"] is not None
        ]

        if not temps:
            raise ValueError("Отсутствуют данные о температуре для расчета среднего значения")

        return round(sum(temps) / len(temps), 1) if temps else None

    def _detect_pressure_warning(self, periods_info: dict) -> str | None:
        """
        Определяет предупреждение о резком перепаде атмосферного давления.

        Note: Правило определения предупреждения о перепаде погоды требует уточнения,
        так как не учтен сценарий с многократным ростом/падением давления в течение дня.
        """
        day_periods = ["Утро", "День", "Вечер", "Ночь"]
        pressures = [
            periods_info[p]["pressure"]
            for p in day_periods
            if periods_info.get(p) and periods_info[p]["pressure"] is not None
        ]

        if not pressures:
            return None

        max_pressure, min_pressure = max(pressures), min(pressures)
        pressure_diff = max_pressure - min_pressure

        if pressure_diff < settings.max_pressure_diff:
            return None

        max_index = pressures.index(max_pressure)
        min_index = pressures.index(min_pressure)

        if max_index < min_index:
            return settings.pressure_warning_fall
        elif max_index > min_index:
            return settings.pressure_warning_raise
        else:
            return None

    def analyze_weather_data(self, raw_data: dict) -> dict:
        """
        Анализирует сырые данные о погоде и возвращает обработанную информацию
        с расчетами и предупреждениями.
        """
        if not raw_data:
            raise ValueError("Получены пустые данные для анализа")

        result = {}

        for date, day_data in raw_data.items():
            periods_info = day_data["periods_info"]

            if not periods_info:
                raise ValueError(f"Отсутствуют данные о периодах дня для {date}")

            mag_field = day_data.get("mag_field")

            avg_temp = self._calculate_average_temp(periods_info)

            pressure_warning = self._detect_pressure_warning(periods_info)

            result[date] = {
                "periods_info": periods_info,
                "whole_day_info": {
                    "avg_day_temp": avg_temp,
                    "mag_field": mag_field
                }
            }

            if pressure_warning:
                result[date]["whole_day_info"]["warning"] = pressure_warning

        return result

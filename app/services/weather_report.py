from sqlalchemy.ext.asyncio import AsyncSession

from app.db.logger import log_report_to_db
from app.db.models import ReportStatus
from app.services.parser import WeatherParser
from app.services.weather import WeatherAnalyzer
from app.services.excel import ExcelWriter
from app.services.file_response import excel_to_streaming_response


class WeatherReportService:
    @staticmethod
    async def create_report(db: AsyncSession, city: str, lat: float, lon: float):
        """
        Формирует Excel-отчет по погоде для указанного города.

        Принимает координаты города и его название, получает данные от парсера,
        передает их для обработки и форматирования, затем формирует отчет в виде Excel-файла.

        В случае возникновения ошибок на любом этапе логируется информация об ошибке.
        При успешном формировании отчета логируется факт успешного выполнения.
        Возвращает файл с расширением .xlsx.
        """
        try:
            parser = WeatherParser(lat, lon)
            raw_data = parser.parse_raw_weather_data()

            analyzer = WeatherAnalyzer()
            processed_data = analyzer.analyze_weather_data(raw_data)

            writer = ExcelWriter(processed_data, city)
            wb = writer.process_excel_file()

            report = excel_to_streaming_response(wb, city)

            await log_report_to_db(db, city, lat, lon, ReportStatus.success)

            return report

        except Exception as e:
            await log_report_to_db(db, city, lat, lon, ReportStatus.error, str(e))
            raise ValueError(f"Не удалось создать отчет для города {city}: {str(e)}") from e



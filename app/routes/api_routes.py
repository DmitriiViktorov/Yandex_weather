import datetime
import io
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse, StreamingResponse
from urllib.parse import quote

from app.services.city_coordinate import city_coordinate
from app.services.parser import WeatherParser
from app.services.weather import WeatherAnalyzer
from app.services.excel import ExcelWriter
from app.services.logger import log_report_to_db
api_router = APIRouter()


@api_router.post("/api/search_city")
async def search_city(city: str = Form(...)):
    """Принимает на вход название города, возвращает список городов с таким названием и их координаты"""
    city_data = city_coordinate(city)
    if not city_data:
        return JSONResponse({"error": "Город не найден"}, status_code=404)
    return {"results": city_data}

@api_router.post("/api/weather_data")
async def weather_data(
        lat: float = Form(...),
        lon: float = Form(...),
        user_city: str = Form(...)
):
    """
    Формирует Excel-отчет по погоде для указанного города.

    Принимает координаты города и его название, получает данные от парсера,
    передает их для обработки и форматирования, затем формирует отчет в виде Excel-файла.

    В случае возникновения ошибок на любом этапе логируется информация об ошибке.
    При успешном формировании отчета логируется факт успешного выполнения.
    Результатом запроса пользователю является файл с расширением .xlsx.
    """
    try:
        parser = WeatherParser(lat, lon)
        raw_weather_data = parser.parse_raw_weather_data()
    except Exception as e:
        log_report_to_db(user_city, lat, lon, "error", f"Parsing error: {e}")
        return {"error": "Error during parsing"}

    try:
        weather_analyzer = WeatherAnalyzer()
        processed_data = weather_analyzer.analyze_weather_data(raw_weather_data)
    except Exception as e:
        log_report_to_db(user_city, lat, lon, "error", f"Analysis error: {e}")
        return {"error": "Error during analysis"}

    try:
        writer = ExcelWriter(processed_data, user_city)
        wb = writer.process_excel_file()
    except Exception as e:
        log_report_to_db(user_city, lat, lon, "error", f"Excel generation error: {e}")
        return {"error": "Error generating Excel"}

    log_report_to_db(user_city, lat, lon, "success")

    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)

    filename = f"Прогноз_{user_city}_{datetime.date.today()}.xlsx"
    filename_encoded = quote(filename)
    headers = {
        "Content-Disposition": f"attachment; filename*=UTF-8''{filename_encoded}"
    }

    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )

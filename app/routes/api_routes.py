import datetime
import io
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse, StreamingResponse
from urllib.parse import quote

from app.services.city_coordinate import city_coordinate
from app.services.parser import WeatherParser
from app.services.weather import WeatherAnalyzer
from app.services.excel import ExcelWriter

api_router = APIRouter()


@api_router.post("/api/search_city")
async def search_city(city: str = Form(...)):
    city_data = city_coordinate(city)
    if not city_data:
        return JSONResponse({"error": "Город не найден"}, status_code=404)
    return {"results": city_data}

@api_router.post("/api/weather_data")
async def weather_data(
        address: str = Form(...),
        lat: float = Form(...),
        lon: float = Form(...),
        user_city: str = Form(...)
):

    parser = WeatherParser(address, lat, lon)
    raw_weather_data = parser.parse_raw_weather_data()

    weather_analyzer = WeatherAnalyzer()
    processed_data = weather_analyzer.analyze_weather_data(raw_weather_data)

    writer = ExcelWriter(processed_data, user_city)
    wb = writer.process_excel_file()

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

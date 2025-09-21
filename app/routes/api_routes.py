from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.city_coordinate import city_coordinate
from app.services.weather_report import WeatherReportService
from app.db.dependencies import get_db
from app.schemas.weather import WeatherRequest


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
        request_data: WeatherRequest,
        db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """
    Формирует отчет о погоде в указанном городе.
    Возвращает в ответ на запрос файл с отчетом в формате .xlsx.
    """
    try:
        report = await WeatherReportService.create_report(
            db,
            request_data.user_city,
            request_data.lat,
            request_data.lon
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return report

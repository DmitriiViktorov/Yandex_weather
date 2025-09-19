import tempfile

from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse, FileResponse

from app.services.city_coordinate import city_coordinate


api_router = APIRouter()


@api_router.post("/api/search_city")
async def search_city(city: str = Form(...)):
    city_data = city_coordinate(city)
    if not city_data:
        return JSONResponse({"error": "Город не найден"}, status_code=404)
    return {"results": city_data}

@api_router.post("/api/weather_data")
async def weather_data(address: str = Form(...), lat: float = Form(...), lon: float = Form(...)):
    file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name

    return FileResponse(
        path=file_path,
        filename="weather_report.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

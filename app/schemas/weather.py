from pydantic import BaseModel

class WeatherRequest(BaseModel):
    lat: float
    lon: float
    user_city: str
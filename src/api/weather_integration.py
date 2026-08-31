from fastapi import APIRouter, status

from api.deps import CityQuery, DbSession
from schemas.weather_schema import WeatherAPISchema, WeatherDBSchema
from services.weather_service import fetch_and_store, fetch_current_weather

router = APIRouter(prefix="/api/openweather", tags=["openweather"])


@router.get(
    "",
    response_model=WeatherAPISchema,
    summary="Clima atual na OpenWeather (não grava)",
)
def get_openweather(city: CityQuery) -> WeatherAPISchema:
    snapshot = fetch_current_weather(city)
    return WeatherAPISchema.model_validate(snapshot)


@router.post(
    "",
    response_model=WeatherDBSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Extrai da OpenWeather e grava no banco",
)
def persist_openweather(db: DbSession, city: CityQuery) -> WeatherDBSchema:
    record = fetch_and_store(db, city)
    return WeatherDBSchema.model_validate(record)

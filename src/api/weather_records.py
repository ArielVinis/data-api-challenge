from fastapi import APIRouter, HTTPException, status

from api.deps import DbSession, WeatherLimit
from schemas.weather_schema import WeatherDBSchema
from services.weather_service import get_record, list_records

router = APIRouter(prefix="/api/weather", tags=["weather-records"])


@router.get(
    "",
    response_model=list[WeatherDBSchema],
    summary="Lista registos climáticos armazenados",
)
def list_weather(
    db: DbSession,
    limit: WeatherLimit = 25,
) -> list[WeatherDBSchema]:
    records = list_records(db, limit=limit)
    return [WeatherDBSchema.model_validate(r) for r in records]


@router.get(
    "/{record_id}",
    response_model=WeatherDBSchema,
    summary="Obtém um registo climático por id",
)
def get_weather(record_id: int, db: DbSession) -> WeatherDBSchema:
    record = get_record(db, record_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Registo {record_id} não encontrado",
        )
    return WeatherDBSchema.model_validate(record)

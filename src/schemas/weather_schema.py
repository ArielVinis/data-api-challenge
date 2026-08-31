from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WeatherAPISchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    city: str
    country: str | None
    temperature_c: float
    humidity: int | None
    description: str | None


class WeatherDBSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city: str
    country: str | None
    temperature_c: float
    humidity: int | None
    description: str | None
    fetched_at: datetime

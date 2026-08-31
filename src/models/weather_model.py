from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class WeatherModel(SQLModel, table=True):
    __tablename__ = "weather"

    id: int | None = Field(default=None, primary_key=True)
    city: str = Field(index=True, max_length=120)
    country: str | None = Field(default=None, max_length=8)
    temperature_c: float
    humidity: int | None = None
    description: str | None = Field(default=None, max_length=255)
    fetched_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        index=True,
    )

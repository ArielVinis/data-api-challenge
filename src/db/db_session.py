from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from config import get_settings
from models.weather_model import WeatherModel

_settings = get_settings()
engine = create_engine(_settings.database_url, echo=False)


def init_db() -> None:
    """Cria tabelas se não existirem."""
    SQLModel.metadata.create_all(engine, tables=[WeatherModel.__table__])


def get_db() -> Generator[Session]:
    with Session(engine) as session:
        yield session

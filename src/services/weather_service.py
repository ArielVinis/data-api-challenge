from dataclasses import dataclass

import httpx
from sqlmodel import Session, col, select

from config import get_settings
from models.weather_model import WeatherModel


class WeatherExternalError(Exception):
    """Falha ao contactar ou interpretar a API OpenWeather."""


@dataclass(frozen=True, slots=True)
class WeatherSnapshot:
    city: str
    country: str | None
    temperature_c: float
    humidity: int | None
    description: str | None


def fetch_current_weather(city: str) -> WeatherSnapshot:
    settings = get_settings()
    if not settings.openweather_api_key:
        raise WeatherExternalError("OPENWEATHER_API_KEY não configurada")

    params = {
        "q": city,
        "appid": settings.openweather_api_key,
        "units": "metric",
        "lang": "pt_br",
    }
    url = f"{settings.openweather_base_url}/weather"

    try:
        with httpx.Client(timeout=10.0) as http:
            response = http.get(url, params=params)
        if response.status_code == 404:
            raise WeatherExternalError(f"Cidade não encontrada: {city}")
        if response.status_code >= 400:
            raise WeatherExternalError(
                f"OpenWeather respondeu {response.status_code}: {response.text}"
            )
        payload = response.json()
    except httpx.HTTPError as exc:
        raise WeatherExternalError(f"Falha de rede na OpenWeather: {exc}") from exc

    weather_list = payload.get("weather") or []
    description = weather_list[0].get("description") if weather_list else None
    main = payload.get("main") or {}
    sys_info = payload.get("sys") or {}

    return WeatherSnapshot(
        city=payload.get("name") or city,
        country=sys_info.get("country"),
        temperature_c=float(main["temp"]),
        humidity=main.get("humidity"),
        description=description,
    )


def save_weather(session: Session, snapshot: WeatherSnapshot) -> WeatherModel:
    record = WeatherModel(
        city=snapshot.city,
        country=snapshot.country,
        temperature_c=snapshot.temperature_c,
        humidity=snapshot.humidity,
        description=snapshot.description,
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


def fetch_and_store(session: Session, city: str) -> WeatherModel:
    snapshot = fetch_current_weather(city)
    return save_weather(session, snapshot)


def list_records(session: Session, *, limit: int = 50) -> list[WeatherModel]:
    statement = (
        select(WeatherModel).order_by(col(WeatherModel.fetched_at).desc()).limit(limit)
    )
    return list(session.exec(statement).all())


def get_record(session: Session, record_id: int) -> WeatherModel | None:
    return session.get(WeatherModel, record_id)

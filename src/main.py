from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import weather_integration, weather_records
from api.exceptions import register_exception_handlers
from db.db_session import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Data API Challenge",
    description="Extração OpenWeather, consulta de dados climáticos e persistência em PostgreSQL.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(weather_integration.router)
app.include_router(weather_records.router)
register_exception_handlers(app)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str | list[str]]:
    return {
        "message": "API de integração com OpenWeather",
        "endpoints": [
            "/health",
            "/docs",
            "/redoc",
        ],
    }

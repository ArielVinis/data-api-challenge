from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from services.weather_service import WeatherExternalError


async def weather_external_error_handler(
    _request: Request,
    exc: WeatherExternalError,
) -> JSONResponse:
    return JSONResponse(
        status_code=502,
        content={"detail": str(exc)},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(WeatherExternalError, weather_external_error_handler)

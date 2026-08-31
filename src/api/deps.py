from typing import Annotated

from fastapi import Depends, Query
from sqlmodel import Session

from db.db_session import get_db

DbSession = Annotated[Session, Depends(get_db)]

CityQuery = Annotated[
    str,
    Query(min_length=1, max_length=120, examples=["São Paulo"]),
]

WeatherLimit = Annotated[int, Query(ge=1, le=100)]

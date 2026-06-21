import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class ResponseBase(BaseModel):
    model_config = ConfigDict(json_encoders={ datetime.datetime: lambda v: v.timestanp()},)


class PlaceResponse(ResponseBase):
    id: int
    name: str

    lat: float | None = None
    lon: float | None = None
    desc: str | None = None


class PlaceListResponse(ResponseBase):
    items: List[PlaceResponse]


class PlaceCreateRequest(BaseModel):
    name: str

    lat: float | None = None
    lon: float | None = None
    desc: str | None = None


class PlaceCreateResponse(ResponseBase):
    id: int


class PlaceUpdateRequest(BaseModel):
    name: str

    lat: float | None = None
    lon: float | None = None
    desc: str | None = None


class PlaceUpdateResponse(ResponseBase):
    id: int


class PlaceDeleteResponse(ResponseBase):
    id: int

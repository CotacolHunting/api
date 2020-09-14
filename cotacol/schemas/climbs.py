from pydantic import BaseModel, ConstrainedInt, HttpUrl, PositiveInt
from typing import List, Literal, Optional


class CotacolId(ConstrainedInt):
    ge = 1
    le = 1000


class Point(BaseModel):
    lat: float
    lon: float
    ele: int


class StravaSegment(BaseModel):
    url: HttpUrl
    confidence: Literal["correct", "toimprove", "toreview", "missing"]


class ClimbExtraData(BaseModel):
    aliases: List[str] = []
    strava_segment: Optional[StravaSegment] = None


class ClimbBase(BaseModel):
    name: str
    city: str
    province: str
    cotacol_points: PositiveInt
    distance: PositiveInt
    elevation_diff: PositiveInt
    avg_grade: float
    extra_data: Optional[ClimbExtraData]


class ClimbUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    cotacol_points: Optional[PositiveInt] = None
    distance: Optional[PositiveInt] = None
    elevation_diff: Optional[PositiveInt] = None
    avg_grade: Optional[float] = None
    extra_data: Optional[ClimbExtraData]


class ClimbList(ClimbBase):
    id: CotacolId
    url: HttpUrl
    polyline: Optional[str] = None

    class Config:
        orm_mode = True


class Climb(ClimbList):
    coordinates: List[Point]

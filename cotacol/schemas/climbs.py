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


class ClimbUpdate(ClimbBase):
    pass


class ClimbList(ClimbBase):
    id: CotacolId
    url: HttpUrl
    polyline: str

    class Config:
        orm_mode = True


class Climb(ClimbList):
    coordinates: List[Point]

import polyline  # type: ignore

from geojson import Feature, LineString  # type: ignore
from sqlalchemy import Column, Float, SmallInteger, String, JSON  # type: ignore
from typing import Optional

from cotacol.db import Base

#  from cotacol.routers.climbs import router


class Climb(Base):
    __tablename__ = "climbs"

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(160))
    city = Column(String(160))
    province = Column(String(160))
    cotacol_points = Column(SmallInteger)
    distance = Column(SmallInteger)
    elevation_diff = Column(SmallInteger)
    avg_grade = Column(Float(precision=3))
    coordinates = Column(JSON)
    extra_data = Column(JSON)

    @property
    def polyline(self) -> Optional[str]:
        if not self.coordinates or not len(self.coordinates):
            return None

        return polyline.encode([(c["lat"], c["lon"], c["ele"]) for c in self.coordinates])

    @property
    def url(self) -> str:
        # TODO: find a way of using `router.url_path_for()`
        return f"https://api.cotacol.cc/v1/climbs/{self.id}/"

    def as_dict(self, *, exclude_coordinates: bool = False) -> dict:
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d["polyline"] = self.polyline
        d["url"] = self.url

        if exclude_coordinates:
            d.pop("coordinates")

        return d

    def as_feature(self) -> Feature:
        geometry = []

        if self.coordinates and len(self.coordinates):
            geometry = LineString([(c["lon"], c["lat"], c["ele"]) for c in self.coordinates])

        properties = self.as_dict(exclude_coordinates=True)
        properties.pop("id")
        properties.pop("polyline")
        properties.pop("url")

        return Feature(id=self.id, geometry=geometry, properties=properties)

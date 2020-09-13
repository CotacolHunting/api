from fastapi import APIRouter, Depends, Security
from fastapi.responses import JSONResponse
from geojson import FeatureCollection  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from typing import List

from cotacol import crud, models, schemas
from cotacol.db import get_db
from cotacol.security import get_user_from_token


router = APIRouter()


@router.get("/cotacol.geojson", summary="Download GeoJSON file")
async def geojson(db: Session = Depends(get_db)):
    """
    Returns a GeoJSON response with all COTACOL climbs as features.
    """
    geojson = FeatureCollection([climb.as_feature() for climb in crud.get_climbs(db)])
    return JSONResponse(content=geojson, media_type="application/geo+json")


@router.get("/", response_model=List[schemas.ClimbList], summary="List all climbs")
async def list_climbs(db: Session = Depends(get_db)):
    """
    Returns the full list of COTACOL climbs. The climbs are returned ordered by the COTACOL id,
    and they don't include the full list of coordinates, just a polyline.
    """
    return crud.get_climbs(db)


@router.get("/{climb_id}/", response_model=schemas.Climb, summary="Retrieve a climb")
async def get_climb(climb_id: schemas.CotacolId, db: Session = Depends(get_db)):
    """
    Retrieves the details of a COTACOL climb with all the information, including coordinates and elevation.
    """
    return crud.get_climb(db, climb_id)


@router.patch("/{climb_id}/", response_model=schemas.Climb, summary="Update a climb")
async def update_climb(
    climb_id: schemas.CotacolId,
    climb: schemas.ClimbUpdate,
    current_user: models.User = Security(get_user_from_token, scopes=["write"]),
    db: Session = Depends(get_db),
):
    stored = models.Climb(**crud.get_climb(db, climb_id))
    updated = stored.copy(update=climb.dict(exclude_unset=True))
    """update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded"""
    return updated

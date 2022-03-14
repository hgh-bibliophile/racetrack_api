from fastapi_crudrouter import OrmarCRUDRouter
from fastapi import HTTPException
from typing import List, Optional

import pydantic
import ormar

from .models import User, Track, Race, Car, Lane, Heat, HeatRun
from . import schema as sch

# ----------
# User
# ----------

users = OrmarCRUDRouter(schema=User)

# ----------
# Track
# ----------

tracks = OrmarCRUDRouter(schema=Track)

@tracks.get('', response_model=List[Track], response_model_exclude={"lanes"})
async def get_all():
    return await Track.objects.select_related(Track.lanes).all()

@tracks.get('/{item_id}', response_model=Track, response_model_exclude={"lanes__track"})
async def get_one(item_id: int):
    return await Track.objects.select_related(Track.lanes).get(pk=item_id)

# Many Lanes: Get, Post

@tracks.get('/{track_id}/lanes', response_model=List[Lane], response_model_exclude={"track"})
async def get_all_track_lanes(track_id: int):
    track = await Track.objects.get(id=track_id)
    return await track.lanes.all()


@tracks.post('/{track_id}/lanes', response_model=List[Lane], response_model_exclude={"track__lanes"})
async def create_many_track_lanes(track_id: int, lanes: List[Lane]):
    track = await Track.objects.get(id=track_id)
    for lane in lanes:
        await track.lanes.add(lane)
    return lanes.dict()

# One Lane: Get, Post

@tracks.get('/{track_id}/lanes/{lane_number_or_id}', response_model=Lane, response_model_exclude={"track"})
async def get_track_lane_by_number_or_id(track_id: int, lane_number_or_id: int, id: bool=False):
    track = await Track.objects.get(id=track_id)
    l_id = lane_number_or_id
    lane = await track.lanes.get(lane_number=l_id) if not id else await track.lanes.get(pk=l_id)
    return lane

@tracks.post('/{track_id}/lane', response_model=Lane, response_model_exclude={"track__lanes"})
async def create_one_track_lane(track_id: int, lane: Lane):
    try:
        track = await Track.objects.get(id=track_id)
        await track.lanes.add(lane)
        return lane.dict()
    except ormar.exceptions.NoMatch as e:
        raise HTTPException(status_code=404, detail=str(e))

# ----------
# Other
# ----------

races = OrmarCRUDRouter(schema=Race)
cars = OrmarCRUDRouter(schema=Car)

# ----------
# Lane - Good
# ----------

lanes = OrmarCRUDRouter(schema=Lane,
    get_all_route=False,
    get_one_route=False,
    create_route=False,
    update_route=False,
    delete_one_route=False,
    delete_all_route=False)

@lanes.get('', response_model=List[sch.LaneReturn_TrackId])
async def get_all():
    return await Lane.objects.all()

@lanes.post("", response_model=sch.LaneReturn_Track)
async def create_item(lane: Lane):
    await lane.save()
    await lane.track.load()
    return lane  # Load Track data

@lanes.delete('')
async def delete_all():
    deleted = 0
    lanes = await Lane.objects.all()
    for lane in lanes:
        await lane.delete()
        deleted += 1
    return {"deleted_rows": deleted}

@lanes.get('/{item_id}', response_model=sch.LaneReturn_Track)
async def get_one(item_id: int):
    try:
        lane = await Lane.objects.get(pk=item_id)
        await lane.track.load()
        return lane
    except ormar.exceptions.NoMatch as e:
        raise HTTPException(status_code=404, detail=f"Not Found: Lane(pk={item_id})")

@lanes.put('/{item_id}', response_model=sch.LaneReturn_Track)
async def update_one(item_id: int, lane: sch.LaneUpdate):
    try:
        update_data = lane.dict(exclude_none=True)
        lane_db = await Lane.objects.get(pk=item_id)
        await lane_db.update(_columns=list(update_data.keys()), **update_data)
        await lane_db.track.load()
        return lane_db
    except ormar.exceptions.NoMatch as e:
        raise HTTPException(status_code=404, detail=f"Not Found: Lane(pk={item_id})")

@lanes.delete('/{item_id}')
async def delete_one(item_id: int, lane: Lane = None):
    try:
        if lane:
            return {"deleted_rows": await lane.delete()}
        lane_db = await Lane.objects.get(pk=item_id)
        return {"deleted_rows": await lane_db.delete()}
    except ormar.exceptions.NoMatch as e:
        raise HTTPException(status_code=404, detail=f"Not Found: Lane(pk={item_id})")

# ----------
# Heat
# ----------

heats = OrmarCRUDRouter(schema=Heat)

@heats.get('/{heat_id}/runs', response_model=List[HeatRun])
async def get_all_heat_runs(heat_id: int):
    heat = await Heat.objects.get(id=heat_id)
    return await heat.runs.all()

# ----------
# HeatRun
# ----------

heat_runs = OrmarCRUDRouter(schema=HeatRun)
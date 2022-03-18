from fastapi_crudrouter import OrmarCRUDRouter
from fastapi import HTTPException, UploadFile
from typing import List, Optional

from ormar.exceptions import NoMatch, ModelError
from pydantic.error_wrappers import ValidationError
from asyncpg.exceptions import UniqueViolationError

from models.track import Track
from models.lane import Lane

from schema.tracks import TrackBase, TrackCreate, TrackReturn, TrackReturnFull, TLane, TLaneUpdate
from schema.lanes import LaneReturn

from .base import exclude_routes, CORSRoute

from utils.routers import get_csv_reader, add_model, invalid_data

# ----------
# Track
# ----------

def not_found(pk: str):
    raise HTTPException(status_code=404, detail=f"Not Found: Track(pk={pk})")

router = OrmarCRUDRouter(schema=Track, route_class=CORSRoute, **exclude_routes)

# Good - Get all Tracks; loads lane_ct but excludes lanes array
@router.get('', response_model=List[TrackReturn])
async def get_all():
    return await Track.objects.select_related(Track.lanes).all()

# Good - Post (insert) a new track, nested saves any lanes
@router.post('', response_model=TrackReturnFull)
async def create_one(track: TrackCreate):
    track = Track(**track.dict())
    await track.save_related()
    return track

# Good - Delete all tracks (and lanes)
@router.delete('')
async def delete_all():
    deleted = Track.objects.count()
    deleted += Lane.objects.count()
    await Track.objects.delete(each=True)
    return {"deleted_rows": deleted}

# Good - Get one track, returns list of lanes
@router.get('/{item_id}', response_model=TrackReturnFull)
async def get_one(item_id: int):
    return await Track.objects.select_related(Track.lanes).get(pk=item_id)

# Good - Update name, NOT Lanes
@router.put('/{item_id}', response_model=TrackReturnFull)
async def update_one(item_id: int, track: TrackBase):
    try:
        update_data = track.dict(exclude_none=True)

        track_db = await Track.objects.select_related(Track.lanes).get(pk=item_id)
        await track_db.update(_columns=list(update_data.keys()), **update_data)

        return track_db
    except NoMatch as e:
        not_found(item_id)

# Good - Delete one tracks (and corresponding lanes)
@router.delete('/{item_id}')
async def delete_one(item_id: int):
    deleted = 0
    try:
        deleted = await Lane.objects.filter(track__id=item_id).count()
        await Track.objects.filter(pk=item_id).delete()
        deleted += 1
        return {"deleted_rows": deleted}
    except NoMatch as e:
        not_found(item_id)

# -----------------
# Get / Create Lanes
# -----------------

# Good - Get list of lanes for one track
@router.get('/{track_id}/lanes', response_model=List[TLane])
async def get_all_track_lanes(track_id: int):
    try:
        track = await Track.objects.get(id=track_id)
        return await track.lanes.all()
    except NoMatch as e:
        not_found(track_id)

# Good - Create & add new lanes to one track -> doesn't return track in response
@router.post('/{track_id}/lanes', response_model=List[TLane])
async def create_track_lanes(track_id: int, lanes: List[TLaneUpdate]):
    try:
        track = await Track.objects.get(id=track_id)
        return await add_model(track.lanes, lanes, Lane)
    except NoMatch as e:
        not_found(track_id)

# Good - Create & add new lanes to one track via csv file
@router.post('/{track_id}/lanes/csv', response_model=List[TLane])
async def create_race_lanes_from_csv_file(track_id: int, csv_lanes: UploadFile):
    try:
        track = await Track.objects.get(id=track_id)
        return await add_model(track.lanes, await get_csv_reader(csv_lanes), Lane)
    except NoMatch as e:
        not_found(track_id)

# -----------------
# Get / Put / Delete Lane
# -----------------

@router.get('/{track_id}/lanes/{lane_num}', response_model=TLane)
async def get_one_track_lane(track_id: int, lane_num: int):
    try:
        track = await Track.objects.get(id=track_id)
        try:
            lane = await track.lanes.get(lane_number=lane_num)
        except NoMatch as e:
            msg = f"Not Found: Lane(lane_number={lane_num}, track_id={track_id})"
            raise HTTPException(status_code=404, detail=msg)
        return lane
    except NoMatch as e:
        not_found(track_id)

@router.put('/{track_id}/lanes/{lane_num}', response_model=TLane)
async def update_one_track_lane(track_id: int, lane_num: int, lane: TLaneUpdate):
    try:
        track = await Track.objects.get(id=track_id)
        try:
            update_data = lane.dict(exclude_none=True)
            lane_db = await track.lanes.get(lane_number=lane_num)
            await lane_db.update(_columns=list(update_data.keys()), **update_data)
            return lane_db
        except NoMatch as e:
            msg = f"Not Found: Lane(lane_number={lane_num}, track_id={track_id})"
            raise HTTPException(status_code=404, detail=msg)
    except NoMatch as e:
        not_found(track_id)



@router.delete('/{track_id}/lanes/{lane_num}', response_model=TLane)
async def delete_one_track_lane(track_id: int, lane_num: int):
    try:
        track = await Track.objects.get(id=track_id)
        try:
            lane = await track.lanes.get(lane_number=lane_num)
            track.lanes.remove(lane, keep_reversed=False)
            deleted = 1
            return {"deleted_rows": deleted}
        except NoMatch as e:
            msg = f"Not Found: Lane(lane_number={lane_num}, track_id={track_id})"
            raise HTTPException(status_code=404, detail=msg)
    except NoMatch as e:
        not_found(track_id)
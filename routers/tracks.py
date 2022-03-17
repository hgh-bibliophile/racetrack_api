from fastapi_crudrouter import OrmarCRUDRouter
from fastapi import HTTPException, Query, Depends
from typing import List, Optional

from ormar.exceptions import NoMatch
from pydantic.error_wrappers import ValidationError
from asyncpg.exceptions import UniqueViolationError

from models.track import Track
from models.lane import Lane

from schema.tracks import TrackUpdate, TrackReturn, TrackReturnFull, TLane, TLaneUpdate
from schema.lanes import LaneReturn

from .base import exclude_routes, CORSRoute

# ----------
# Track
# ----------

def not_found(pk: str):
    raise HTTPException(status_code=404, detail=f"Not Found: Track(pk={pk})")

def invalid_data(msg):
    raise HTTPException(status_code=422, detail=msg)

router = OrmarCRUDRouter(schema=Track, route_class=CORSRoute, **exclude_routes)

# Good - Get all Tracks; loads lane_ct but excludes lanes array
@router.get('', response_model=List[TrackReturn])
async def get_all():
    return await Track.objects.select_related(Track.lanes).all()

# Good - Post (insert) a new track, nested saves any lanes
@router.post('', response_model=TrackReturnFull)
async def create_one(track: TrackUpdate):
    await track.save_related()
    return track

# Good - Delete all tracks (and lanes)
@router.delete('')
async def delete_all():
    deleted = 0
    deleted += await Track.objects.delete(each=True)
    deleted += await Lane.objects.delete(each=True)
    return {"deleted_rows": deleted}

# Good - Get one track, returns list of lanes
@router.get('/{item_id}', response_model=TrackReturnFull)
async def get_one(item_id: int):
    return await Track.objects.select_related(Track.lanes).get(pk=item_id)

# Mostly Good - Better error checking on insert vs update lanes
@router.put('/{item_id}', response_model=TrackReturnFull)
async def update_one(item_id: int, track: TrackUpdate):
    try:
        update_data = track.dict(exclude_none=True)
        update_lanes = update_data.pop('lanes', [])

        track_db = await Track.objects.get(pk=item_id)
        await track_db.update(_columns=list(update_data.keys()), **update_data)

        err_lanes = []
        for lane in update_lanes:
            if 'id' in lane:
                t_lane = await track_db.lanes.get(pk=lane.pop('id'))
                await t_lane.update(_columns=lane.keys(), **lane)
            else:
                try:
                    t_lane = Lane(**lane)
                    await track_db.lanes.add(t_lane)
                except ValidationError as e:
                    err_lanes.append(lane)
                except UniqueViolationError as e:
                    invalid_data(e.detail)

        if len(err_lanes) > 0:
            msg = {
                'msg': f"Unprocessable lanes. Check that all required fields are present.",
                'track_id': item_id,
                'err_data': err_lanes
            }
            invalid_data(msg)

        await track_db.lanes.all()
        return track_db
    except NoMatch as e:
        not_found(item_id)

# Good - Delete one tracks (and corresponding lanes)
@router.delete('/{item_id}')
async def delete_one(item_id: int):
    deleted = 0
    try:
        track = await Track.objects.select_related(Track.lanes).get(pk=item_id)
        deleted += track.lanes_ct
        await track.lanes.clear(keep_reversed=False)
        await track.delete()
        deleted += 1
        return {"deleted_rows": deleted}
    except NoMatch as e:
        not_found(item_id)

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
        for lane in lanes:
            await track.lanes.add(lane)
        return lanes
    except NoMatch as e:
        not_found(track_id)

# One Lane: Get, Post
async def id_or_number(
    id: Optional[int] = Query(None), lane_num: Optional[int] = Query(None)
) -> dict:
    if not id and not lane_num:
        raise HTTPException(status_code=400, detail="must provide id or lane_num")
    if id and lane_num:
        raise HTTPException(status_code=400, detail="must not provide both id and lane_num")

    key = "id" if id else "lane_number"
    val = id if id else lane_num
    return {key: val}


@router.get('/{track_id}/lane', response_model=TLane)
async def get_one_track_lane(track_id: int, filter: dict = Depends(id_or_number)):
    try:
        track = await Track.objects.get(id=track_id)
        try:
            lane = await track.lanes.get(**filter)
        except NoMatch as e:
            lane_filter = ",".join(f'{k}={v}' for k,v in filter.items())
            msg = f"Not Found: Lane({lane_filter}) for Track(pk={track_id})"
            raise HTTPException(status_code=404, detail=msg)
        return lane
    except NoMatch as e:
        not_found(track_id)


@router.post('/{track_id}/lane', response_model=TLane)
async def create_one_track_lane(track_id: int, lane: TLaneUpdate):
    try:
        track = await Track.objects.get(id=track_id)
        await track.lanes.add(lane)
        return lane.dict()
    except NoMatch as e:
        not_found(track_id)
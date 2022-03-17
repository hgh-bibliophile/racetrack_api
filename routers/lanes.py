from fastapi_crudrouter import OrmarCRUDRouter
from fastapi import HTTPException
from typing import List

from ormar.exceptions import NoMatch

from models.lane import Lane

from schema.lanes import LaneReturn, LaneReturn_Track, LaneReturn_TrackId, LaneUpdate

from .base import exclude_routes, CORSRoute

# ----------
# Lane - Good
# ----------

def not_found(pk: str):
    raise HTTPException(status_code=404, detail=f"Not Found: Lane(pk={pk})")

router = OrmarCRUDRouter(schema=Lane, route_class=CORSRoute, **exclude_routes)

@router.get('', response_model=List[LaneReturn_TrackId])
async def get_all():
    return await Lane.objects.all()

@router.post("", response_model=LaneReturn_Track)
async def create_item(lane: Lane):
    await lane.save()
    await lane.track.load()  # Load Track data
    return lane

@router.delete('')
async def delete_all():
    deleted = 0
    lanes = await Lane.objects.all()
    for lane in lanes:
        await lane.delete()
        deleted += 1
    return {"deleted_rows": deleted}

@router.get('/{item_id}', response_model=LaneReturn_Track)
async def get_one(item_id: int):
    try:
        lane = await Lane.objects.get(pk=item_id)
        await lane.track.load()
        return lane
    except NoMatch as e:
        not_found(item_id)

@router.put('/{item_id}', response_model=LaneReturn_Track)
async def update_one(item_id: int, lane: LaneUpdate):
    try:
        update_data = lane.dict(exclude_none=True)
        lane_db = await Lane.objects.get(pk=item_id)
        await lane_db.update(_columns=list(update_data.keys()), **update_data)
        await lane_db.track.load()
        return lane_db
    except NoMatch as e:
        not_found(item_id)

@router.delete('/{item_id}')
async def delete_one(item_id: int, lane: Lane = None):
    try:
        if not lane:
            lane = await Lane.objects.get(pk=item_id)
        return {"deleted_rows": await lane.delete()}
    except NoMatch as e:
        not_found(item_id)
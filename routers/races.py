from fastapi_crudrouter import OrmarCRUDRouter
from typing import List
from models.race import Race
from schema.races import RaceUpdate, RaceReturnId, RaceReturnFull
from .base import exclude_routes, CORSRoute

router = OrmarCRUDRouter(schema=Race, route_class=CORSRoute)

# Return format - Get all Races; loads related_ct, excludes related arrays
@router.get('', response_model=List[RaceReturnId])
async def get_all():
    return await Race.objects.select_all().all()

# (Return format) - Post (insert) a new race, saves nested objects
@router.post('', response_model=RaceReturnFull)
async def create_one(race: RaceUpdate):
    await race.save_related(follow=True)
    return race

# Return format - Get one track, returns list of lanes
@router.get('/{item_id}', response_model=RaceReturnFull)
async def get_one(item_id: int):
    return await Race.objects.select_all().get(pk=item_id)
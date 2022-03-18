from fastapi_crudrouter import OrmarCRUDRouter
from typing import List



from models.heat import Heat
from models.heat_run import HeatRun

from schema.heats import HeatBase, HeatCreate, HeatReturn, HeatReturnFull, HeatReturnIds

from .base import exclude_routes, CORSRoute


from utils.routers import update_model

def not_found(pk: str):
    raise HTTPException(status_code=404, detail=f"Not Found: Heat(pk={pk})")


router = OrmarCRUDRouter(schema=Heat, route_class=CORSRoute)

# Good - Get all heats; loads lane_ct but excludes lanes array
@router.get('', response_model=List[HeatReturn])
async def get_all():
    return await Heat.objects.select_all().all()

# Good - Post (insert) a new heat, nested saves any lanes
@router.post('', response_model=HeatReturnFull)
async def create_one(heat: HeatCreate):
    heat = Heat(**heat.dict())
    await heat.save_related()
    return heat

# Good - Delete all heats (and heatruns)
@router.delete('')
async def delete_all():
    deleted = await Heat.objects.count()
    deleted += await HeatRun.objects.count()
    await Heat.objects.delete(each=True)
    return {"deleted_rows": deleted}

# Good - Get one heat w/ full details
@router.get('/{item_id}', response_model=HeatReturnFull)
async def get_one(item_id: int):
    return await Heat.objects.select_all().get(pk=item_id)

# Good - Update name, NOT Lanes
@router.put('/{item_id}', response_model=HeatReturnFull)
async def update_one(item_id: int, heat: HeatBase):
    try:
        heat_db = await Heat.objects.select_all().get(pk=item_id)
        await update_model(heat_db, heat)
        return heat_db
    except NoMatch as e:
        not_found(item_id)

# Good - Delete one heat (and corresponding heatruns)
@router.delete('/{item_id}')
async def delete_one(item_id: int):
    deleted = 0
    try:
        deleted = await HeatRun.objects.filter(heat__id=item_id).count()
        await Heat.objects.filter(pk=item_id).delete()
        deleted += 1
        return {"deleted_rows": deleted}
    except NoMatch as e:
        not_found(item_id)

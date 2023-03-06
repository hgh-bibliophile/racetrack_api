from fastapi_crudrouter import OrmarCRUDRouter

from ormar.exceptions import NoMatch

from models.heat_run import HeatRun

from .base import CORSRoute

router = OrmarCRUDRouter(schema=HeatRun, route_class=CORSRoute)

# Good - Delete all heatruns
@router.delete('')
async def delete_all():
    deleted = await HeatRun.objects.count()
    await HeatRun.objects.delete(each=True)
    return {"deleted_rows": deleted}


# Good - Delete one heatrun
@router.delete('/{item_id}')
async def delete_one(item_id: int):
    deleted = 0
    try:
        await HeatRun.objects.filter(pk=item_id).delete()
        deleted += 1
        return {"deleted_rows": deleted}
    except NoMatch as e:
        not_found(item_id)
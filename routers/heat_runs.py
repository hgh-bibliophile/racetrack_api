from fastapi_crudrouter import OrmarCRUDRouter

from models.heat_run import HeatRun

from .base import CORSRoute

router = OrmarCRUDRouter(schema=HeatRun, route_class=CORSRoute)

# Good - Delete all heatruns
@router.delete('')
async def delete_all():
    deleted = await HeatRun.objects.count()
    await HeatRun.objects.delete(each=True)
    return {"deleted_rows": deleted}
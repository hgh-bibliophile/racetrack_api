from fastapi_crudrouter import OrmarCRUDRouter

from models.heat_run import HeatRun


router = OrmarCRUDRouter(schema=HeatRun)

# Good - Delete all heatruns
@router.delete('')
async def delete_all():
    deleted = await HeatRun.objects.count()
    await HeatRun.objects.delete(each=True)
    return {"deleted_rows": deleted}
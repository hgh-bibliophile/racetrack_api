from fastapi_crudrouter import OrmarCRUDRouter
from typing import List

from models.car import Car

from schema.cars import CarBase, CarCreate, CarReturn, CarReturnFull, CarReturnIds

from .base import CORSRoute

router = OrmarCRUDRouter(schema=Car, route_class=CORSRoute)

# Good - Get all cars; loads lane_ct but excludes lanes array
@router.get('', response_model=List[CarReturn])
async def get_all():
    return await Car.objects.select_all().all()
    
# Good - Post (insert) a new car, nested saves any lanes
@router.post('', response_model=CarReturnFull)
async def create_one(car: CarCreate):
    car = Car(**car.dict())
    await car.save_related()
    return car

# Good - Delete all cars (and carruns)
@router.delete('')
async def delete_all():
    deleted = await Car.objects.count()
    deleted += await CarRun.objects.count()
    await Car.objects.delete(each=True)
    return {"deleted_rows": deleted}

# Good - Get one car w/ full details
@router.get('/{item_id}', response_model=CarReturnFull)
async def get_one(item_id: int):
    return await Car.objects.select_all().get(pk=item_id)

# Good - Update name, NOT Lanes
@router.put('/{item_id}', response_model=CarReturnFull)
async def update_one(item_id: int, car: CarBase):
    try:
        car_db = await Car.objects.select_all().get(pk=item_id)
        await update_model(car_db, car)
        return car_db
    except NoMatch as e:
        not_found(item_id)

# Good - Delete one car (and corresponding carruns)
@router.delete('/{item_id}')
async def delete_one(item_id: int):
    deleted = 0
    try:
        deleted = await CarRun.objects.filter(car__id=item_id).count()
        await Car.objects.filter(pk=item_id).delete()
        deleted += 1
        return {"deleted_rows": deleted}
    except NoMatch as e:
        not_found(item_id)
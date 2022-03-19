from fastapi_crudrouter import OrmarCRUDRouter
from fastapi import HTTPException, Query, Depends, UploadFile
from typing import List, Optional

from datetime import datetime

from ormar.exceptions import NoMatch, ModelError
from pydantic.error_wrappers import ValidationError
from asyncpg.exceptions import UniqueViolationError

from models.race import Race
from models.car import Car
from models.heat import Heat
from models.heat_run import HeatRun

from schema.races import RaceCreate, RaceUpdate, RaceReturnId, RaceReturnFull, RaceReturnUpdate, RCar, RCarCreate, RHeat, RHeatCreate, RHeatRunIds, RHeatUpdate, RHeatRunUpdateIds, RCarSpeed

from .base import exclude_routes, CORSRoute
from .ws import get_heat_runs, update_heat_runs

from utils.routers import get_csv_reader, add_model, invalid_data, catch_errors

def not_found(pk: str):
    raise HTTPException(status_code=404, detail=f"Not Found: Race(pk={pk})")

router = OrmarCRUDRouter(schema=Race, route_class=CORSRoute, **exclude_routes)

# Good - Get all Races; loads related_ct, excludes related arrays
@router.get('', response_model=List[RaceReturnId])
async def get_all():
    return await Race.objects.select_all().all()

# Good - Post (insert) a new race, saves nested objects
@router.post('', response_model=RaceReturnFull)
async def create_one(race: RaceCreate):
    race = Race(**race.dict(exclude_none=True))
    await race.save_related(follow=True)
    if race.owner: await race.owner.load()
    if race.track: await race.track.load()
    return race

# Good - Delete all races (and cars, heats, heatruns)
@router.delete('')
async def delete_all():
    deleted = await Race.objects.count()
    deleted += await Car.objects.count()
    deleted += await Heat.objects.count()
    deleted += await HeatRun.objects.count()
    await Race.objects.delete(each=True)
    return {"deleted_rows": deleted}

# Get - Get one race, returns w/ list of cars
@router.get('/l/{race_link}', response_model=RaceReturnId)
async def get_one(race_link: str):
    try:
        return await Race.objects.select_all().get(watch_link=race_link)
    except NoMatch as e:
        raise HTTPException(status_code=404, detail=f"Not Found: Race({race_link})")

# Get - Get one race, returns w/ list of cars
@router.get('/{item_id}', response_model=RaceReturnFull)
async def get_one(item_id: int):
    return await Race.objects.prefetch_related([Race.track.lanes, Race.owner, Race.heats, Race.cars.runs]).get(pk=item_id)

# Good - Update fields + fk ids - NO reverse relations
@router.put('/{item_id}', response_model=RaceReturnUpdate)
async def update_one(item_id: int, race: RaceUpdate):
    try:
        update_data = race.dict(exclude_none=True)
        race_db = await Race.objects.select_all().get(pk=item_id)
        await race_db.update(_columns=list(update_data.keys()), **update_data)
        return race_db
    except NoMatch as e:
        not_found(item_id)

# Good - Delete one race (and corresponding cars, heats, and heatruns)
@router.delete('/{item_id}')
async def delete_one(item_id: int):
    deleted = 0
    try:
        deleted += await Car.objects.filter(race__id=item_id).count()
        deleted += await Heat.objects.filter(race__id=item_id).count()
        deleted += await HeatRun.objects.filter(heat__race__id=item_id).count()
        await Race.objects.filter(pk=item_id).delete(each=True)
        deleted += 1
        return {"deleted_rows": deleted}
    except NoMatch as e:
        not_found(item_id)

# -----------------
# Get / Create Cars
# -----------------

# Good - Get list of cars for one race
@router.get('/{race_id}/cars', response_model=List[RCar])
async def get_all_race_cars(race_id: int):
    try:
        return await Car.objects.prefetch_related([Car.runs]).filter(race__id=race_id).all()
    except NoMatch as e:
        not_found(race_id)

# Good - Get list of cars + speeds for one race
@router.get('/{race_id}/speeds', response_model=List[RCarSpeed])
async def get_all_race_cars(race_id: int):
    try:
        return await Car.objects.prefetch_related([Car.runs.lane]).filter(race__id=race_id).all()
    except NoMatch as e:
        not_found(race_id)


# Good - Delete all cars
@router.delete('/{race_id}/cars')
async def delete_all_race_cars(race_id: int):
    deleted = 0
    try:
        deleted += await Car.objects.filter(race__id=race_id).count()
        deleted += await HeatRun.objects.filter(heat__race__id=race_id).count()
        #deleted += await Heat.objects.filter(race__id=race_id).count()
        await Car.objects.filter(pk=race_id).delete(each=True)
        #await Heat.objects.filter(pk=race_id).delete(each=True)
        return {"deleted_rows": deleted}
    except NoMatch as e:
        not_found(race_id)

# Good - Create & add new cars to one race -> doesn't return race in response
@router.post('/{race_id}/cars', response_model=List[RCar])
async def create_race_cars(race_id: int, cars: List[RCarCreate]):
    try:
        race = await Race.objects.get(pk=race_id)
        return await add_model(race.cars, cars, Car)
    except NoMatch as e:
        not_found(race_id)

# Good - Create & add new cars to one race via csv file
@router.post('/{race_id}/cars/csv', response_model=List[RCar])
async def create_race_cars_from_csv_file(race_id: int, csv_cars: UploadFile):
    try:
        race = await Race.objects.get(id=race_id)
        return await add_model(race.cars, await get_csv_reader(csv_cars), Car)
    except NoMatch as e:
        not_found(race_id)

# -----------------
# Get / Put / Delete Car
# -----------------

@router.get('/{race_id}/cars/{car_num}', response_model=RCar)
async def get_one_race_car(race_id: int, car_num: int):
    try:
        race = await Race.objects.get(id=race_id)
        try:
            car = await race.cars.prefetch_related(Car.runs).get(car_number=car_num)
        except NoMatch as e:
            msg = f"Not Found: Car(car_number={car_num}, race_id={race_id})"
            raise HTTPException(status_code=404, detail=msg)
        return car
    except NoMatch as e:
        not_found(race_id)

@router.put('/{race_id}/cars/{car_num}', response_model=RCar)
async def update_one_race_car(race_id: int, car_num: int, car: RCarCreate):
    try:
        race = await Race.objects.get(id=race_id)
        try:
            update_data = car.dict(exclude_none=True)
            car_db = await race.cars.get(car_number=car_num)
            await car_db.update(_columns=list(update_data.keys()), **update_data)
            return car_db
        except NoMatch as e:
            msg = f"Not Found: Car(car_number={car_num}, race_id={race_id})"
            raise HTTPException(status_code=404, detail=msg)
    except NoMatch as e:
        not_found(race_id)

@router.delete('/{race_id}/cars/{car_num}')
async def delete_one_race_car(race_id: int, car_num: int):
    try:
        race = await Race.objects.get(id=race_id)
        try:
            car = await race.cars.get(car_number=car_num)
            deleted = await car.runs.count()
            await race.cars.remove(car, keep_reversed=False)
            deleted += 1
            return {"deleted_rows": deleted}
        except NoMatch as e:
            msg = f"Not Found: Car(car_number={car_num}, race_id={race_id})"
            raise HTTPException(status_code=404, detail=msg)
    except NoMatch as e:
        not_found(race_id)


# -----------------
# Get / Create Heats
# -----------------

# Good - Get list of heats for one race
@router.get('/{race_id}/heats', response_model=List[RHeat])
async def get_all_race_heats(race_id: int):
    try:
        return await Heat.objects.prefetch_related([Heat.runs.car, Heat.runs.lane]).filter(race__id=race_id).all()
    except NoMatch as e:
        not_found(race_id)

# Good - Delete all heats
@router.delete('/{race_id}/heats')
async def delete_all_race_heats(race_id: int):
    deleted = 0
    try:
        deleted += await Heat.objects.filter(race__id=race_id).count()
        deleted += await HeatRun.objects.filter(heat__race__id=race_id).count()
        await Heat.objects.delete(race__id=race_id)
        return {"deleted_rows": deleted}
    except NoMatch as e:
        not_found(race_id)

# Good - Create & add new heats to one race -> doesn't return race in response
@router.post('/{race_id}/heats', response_model=List[RHeat])
async def create_race_heats(race_id: int, heats: List[RHeatCreate]):
    try:
        race = await Race.objects.select_related([Race.track.lanes, Race.cars]).get(pk=race_id)
        if race.track == None:
            return invalid_data(f'Race(pk={race_id}) does not have a valid track. Please assign a track before creating HeatRuns.')

        lanes = {l.lane_number: l.id for l in await race.track.lanes.all()}
        cars = {c.car_number: c.id for c in await race.cars.all()}

        new_heats = []
        run_data = {}

        for heat in heats:
            heat_data = heat.dict(exclude_none=True)
            heat_num = heat_data.get('heat_number')
            run_data[int(heat_num)] = heat_data.pop('runs', [])
            new_heats.append(Heat(race=race.id, heat_number=heat_num))

        heat_numbers = run_data.keys()

        err = []
        async def create_heats():
            await Heat.objects.bulk_create(new_heats)
            heats = await Heat.objects.fields(['heat_number']).all(Heat.heat_number << heat_numbers)

            new_runs = []
            for heat in heats:
                for run in run_data.get(heat.heat_number, {}):
                    new_runs.append(HeatRun(
                        heat=heat.id,
                        lane=lanes.get(run.get('lane_number')),
                        car=cars.get(run.get('car_number'))
                    ))

            await HeatRun.objects.bulk_create(new_runs)

        await catch_errors(create_heats, err)
        if len(err) > 0:
            return invalid_data(err)

        return await Heat.objects.prefetch_related([Heat.runs.car, Heat.runs.lane]).all(Heat.heat_number << heat_numbers)

    except NoMatch as e:
        not_found(race_id)

# Good - Create & add new heats to one race via csv file
@router.post('/{race_id}/heats/csv', response_model=List[RHeat])
async def create_race_heats_from_csv_file(race_id: int, csv_heats: UploadFile):
    try:
        reader = await get_csv_reader(csv_heats)
        race = await Race.objects.prefetch_related([Race.track.lanes, Race.cars]).get(id=race_id)
        if race.track == None:
            return invalid_data(f'Race(pk={race_id}) does not have a valid track. Please assign a track before creating HeatRuns.')

        lanes = {str(l.lane_number): l.id for l in await race.track.lanes.all()}
        cars = {str(c.car_number): c.id for c in await race.cars.all()}

        new_heats = []
        run_data = {}
        for heat_data in reader:
            heat_num = heat_data.pop('heat_number')
            run_data[int(heat_num)] = heat_data.items()
            new_heats.append(Heat(race=race.id, heat_number=heat_num))

        heat_numbers = run_data.keys()

        err = []
        async def create_heats():
            await Heat.objects.bulk_create(new_heats)
            heats = await Heat.objects.fields(['heat_number']).all((Heat.race.id == race.id) & (Heat.heat_number << heat_numbers))

            new_runs = []
            for heat in heats:
                for lane_num, car_num in run_data.get(heat.heat_number, {}):
                    new_runs.append(HeatRun(
                        heat=heat.id,
                        lane=lanes.get(lane_num),
                        car=cars.get(car_num)
                    ))

            await HeatRun.objects.bulk_create(new_runs)

        await catch_errors(create_heats, err)
        if len(err) > 0:
            return invalid_data(err)

        return await Heat.objects.prefetch_related([Heat.runs.car, Heat.runs.lane]).all(Heat.heat_number << heat_numbers)

    except NoMatch as e:
        not_found(race_id)

# -----------------
# Get / Put / Delete Heat
# -----------------

@router.get('/{race_id}/heats/{heat_num}', response_model=RHeat)
async def get_one_race_heat(race_id: int, heat_num: int):
    try:
        race = await Race.objects.get(id=race_id)
        try:
            heat = await race.heats.prefetch_related([Heat.runs.car, Heat.runs.lane]).get(heat_number=heat_num)
        except NoMatch as e:
            msg = f"Not Found: Heat(heat_number={heat_num}, race_id={race_id})"
            raise HTTPException(status_code=404, detail=msg)
        return heat
    except NoMatch as e:
        not_found(race_id)

@router.put('/{race_id}/heats/{heat_num}', response_model=RHeat)
async def update_one_race_heat(race_id: int, heat_num: int, heat: RHeatUpdate):
    try:
        race = await Race.objects.select_related([Race.track, Race.cars]).get(pk=race_id)
        if race.track == None:
            return invalid_data(f'Race(pk={race_id}) does not have a valid track. Please assign a track before editing HeatRuns.')

        lanes = {l.lane_number: l for l in await race.track.lanes.all()}
        cars = {c.car_number: c for c in await race.cars.all()}

        try:
            update_data = heat.dict(exclude_none=True)
            runs = update_data.pop('runs', [])

            heat_db = await race.heats.get(heat_number=heat_num)
            await heat_db.update(_columns=list(update_data.keys()), **update_data)

            err = []
            for run in runs:
                async def upsert_runs():
                    if 'lane_number' in run:
                        run['lane'] = lanes.get(run.pop('lane_number'))
                    if 'car_number' in run:
                        run['car'] = cars.get(run.pop('car_number'))

                    if 'id' in run:
                        heatrun = await heat_db.runs.get(pk=run.pop('id'))
                        await heatrun.update(_columns=list(run.keys()), **run)
                    else:
                        await heat_db.runs.add(HeatRun(**run))

                await catch_errors(upsert_runs, err)

            await heat_db.runs.select_related([HeatRun.lane, HeatRun.car]).all()
            return heat_db if len(err) == 0 else invalid_data(err)
        except NoMatch as e:
            msg = f"Not Found: Heat(heat_number={heat_num}, race_id={race_id})"
            raise HTTPException(status_code=404, detail=msg)

    except NoMatch as e:
        not_found(race_id)

@router.delete('/{race_id}/heats/{heat_num}')
async def delete_one_race_heat(race_id: int, heat_num: int):
    try:
        race = await Race.objects.get(id=race_id)
        try:
            heat = await race.heats.get(heat_number=heat_num)
            deleted = await heat.runs.count()
            await race.heats.remove(heat, keep_reversed=False)
            deleted += 1
            return {"deleted_rows": deleted}
        except NoMatch as e:
            msg = f"Not Found: Heat(heat_number={heat_num}, race_id={race_id})"
            raise HTTPException(status_code=404, detail=msg)
    except NoMatch as e:
        not_found(race_id)


@router.get('/{race_id}/heats/{heat_num}/runs', response_model=List[RHeatRunIds])
async def get_all_race_heat_runs(race_id: int, heat_num: int):
    try:
        race = await Race.objects.get(id=race_id)
        return await get_heat_runs(race, heat_num)

    except NoMatch as e:
        not_found(race_id)

@router.put('/{race_id}/heats/{heat_num}/runs', response_model=list[RHeatRunIds])
async def update_all_race_heat_runs(race_id: int, heat_num: int, runs: List[RHeatRunUpdateIds]):
    try:
        race = await Race.objects.get(pk=race_id)
        return await update_heat_runs(race, heat_num, runs)

    except NoMatch as e:
        not_found(race_id)

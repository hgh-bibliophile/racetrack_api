from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import List

from datetime import datetime

from ormar.exceptions import NoMatch, ModelError

from utils.ws import ConnectionManager
from utils.routers import catch_errors

from models.race import Race
from models.heat import Heat
from models.heat_run import HeatRun

from schema.ws import WS_HeatRun, WS_HeatRunUpdate
from schema.races import RHeatRunIds, RHeatRunUpdateIds

from .base import CORSRoute

router = APIRouter(
  prefix="/ws",
  tags=["Websockets"],
  responses={404: {"description": "Not found"}},
  route_class=CORSRoute
)

manager = ConnectionManager()

async def get_heat_runs(race: Race, heat_num: int):
    try:
        heat = await race.heats.get(heat_number=heat_num)
        return [await run_ids(run) for run in await heat.runs.prefetch_related([HeatRun.lane, HeatRun.car]).all()]
    except NoMatch as e:
        msg = f"Not Found: Heat(heat_number={heat_num}, race_id={race_id})"
        raise HTTPException(status_code=404, detail=msg)

async def update_heat_runs(race: Race, heat_num: int, runs: List[WS_HeatRunUpdate]):
    try:
        heat_db = await race.heats.get(heat_number=heat_num)
        await heat_db.update(ran_at=datetime.now())
        heat_runs = {r.id: r for r in await heat_db.runs.prefetch_related([HeatRun.lane, HeatRun.car]).all()}

        err = []
        _runs = []
        for run in runs:
            heatrun = heat_runs.get(run.id)
            heatrun.delta_ms = run.delta_ms
            _runs.append(heatrun)

        async def update_runs():
            await HeatRun.objects.bulk_update(_runs)

        await catch_errors(update_runs, err)

        run_data = []
        for run in heat_runs.values():
            run_data.append(await run_ids(run))

        return run_data if len(err) == 0 else invalid_data(err)
    except NoMatch as e:
        msg = f"Not Found: Heat(heat_number={heat_num}, race_id={race.id})"
        raise HTTPException(status_code=404, detail=msg)

async def run_ids(heat_run: HeatRun):
    return WS_HeatRun(**heat_run.dict())

def ws_data(heat_num, heat_data):
    return {
        'heat_number': heat_num,
        'runs': [r.dict() for r in heat_data]
    }

# Register a regular HTTP route
@router.get("/{race_link}/heat/{heat_num}", response_model=list[WS_HeatRun])
async def start_heat(race_link: str, heat_num: int):
    try:
        race = await Race.objects.get(watch_link=race_link)
        heat_data =  await get_heat_runs(race, heat_num)
        await manager.broadcast(race_link, 'start_heat', ws_data(heat_num, heat_data))
        return heat_data
    except NoMatch as e:
        not_found(race_id)
    return await Heat.objects.filter(race__watch_link=race_link, heat_number=heat_num).get()

@router.put('/{race_link}/heat/{heat_num}', response_model=list[WS_HeatRun])
async def end_heat(race_link: str, heat_num: int, runs: List[WS_HeatRunUpdate]):
    try:
        race = await Race.objects.get(watch_link=race_link)
        heat_data = await update_heat_runs(race, heat_num, runs)

        await manager.broadcast(race_link, 'heat_results', ws_data(heat_num, heat_data))
        return heat_data

    except NoMatch as e:
        not_found(race_id)


@router.websocket("/watch/{race_link}")
async def websocket_endpoint(websocket: WebSocket, race_link: str):
    await manager.connect(race_link, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(race_link, websocket)
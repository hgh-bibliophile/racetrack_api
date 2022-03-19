import csv
from fastapi import HTTPException, UploadFile
from typing import List

from ormar.exceptions import NoMatch, ModelError
from pydantic.error_wrappers import ValidationError
from asyncpg.exceptions import UniqueViolationError

def invalid_data(msg):
    raise HTTPException(status_code=422, detail=msg)

async def catch_errors(func, err):
    try:
        return await func()
    except UniqueViolationError as e:
        err.append(e.detail)
    except ValidationError as e:
        err.append(str(e).replace('\n', '.', 1).replace('\n', ':'))
    except ModelError as e:
        invalid_data(str(e))


async def get_csv_reader(file: UploadFile):
    csv_str = await file.read()
    csv_list = csv_str.decode('utf-8').split('\n')
    return csv.DictReader(csv_list, skipinitialspace=True)

async def add_model(parent_array: List, child_data, child_class):
    err = []
    results = []
    for i, child in enumerate(child_data):
        try:
            if not isinstance(child, dict):
                child = child.dict(exclude_none=True)
            child = child_class(**child)
            await parent_array.add(child)
            results.append(child)
        except UniqueViolationError as e:
            err.append(e.detail)
        except ValidationError as e:
            msg = {
                'msg': str(e).replace('\n', '.', 1).replace('\n', ':'),
                'data': child
            }
            err.append(msg)
        except ModelError as e:
            invalid_data(str(e))

    if len(err) > 0:
        return invalid_data(err)

    return results

async def update_model(object, data_model):
    data = data_model.dict(exclude_none=True)
    await object.update(_columns=list(update_data.keys()), **update_data)

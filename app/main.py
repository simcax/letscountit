from fastapi import FastAPI
from fastapi.responses import JSONResponse
from letscountit.base import Counterthing
from letscountit.db.edgedb import Database
from uuid import UUID
import json
app = FastAPI()


@app.get('/counter/{uuid}')
def get_counter(uuid: str):
    db = Database()
    result = db.get_counter(uuid)
    result_dict = {'uuid': str(UUID(result.uuid.hex)), 'name': result.name, 'count': result.count}
    return JSONResponse(content=result_dict)


@app.post('/counter/new/{uuid}/{name}')
def add_new_counter(uuid: UUID, name: str):
    db = Database()
    result = db.insert_counter(uuid, name)
    result_dict = {'uuid': str(UUID(result.id.hex))}
    return JSONResponse(content=result_dict)

@app.post('/counter/create/{name}/{count}')
def create_counter(name: str, count: int = 0):
    db = Database()
    counter = Counterthing(name=name)
    result = db.create_counter(name, count)
    uuid = str(UUID((result.uuid.hex)))
    result_dict = {'uuid': f"{uuid}", 'name': f"{result.name}", 'count': f"{result.count}"}
    return JSONResponse(content=result_dict)

@app.post('/counter/increase/{uuid}')
def increase_counter(uuid: str):
    """Increase the count of a counter by 1."""
    db = Database()
    # Get the current count of the counter
    result = db.get_counter(uuid)
    # Increase the count by 1
    count = result.count + 1
    result = db.update_counter(uuid, count)
    current_counter = db.get_counter(uuid)

    result_dict = {'uuid': str(UUID(current_counter.uuid.hex)), 'name': current_counter.name, 'count': current_counter.count}
    return JSONResponse(content=result_dict)

@app.post('/counter/decrease/{uuid}')
def decrease_counter(uuid: str):
    """Decrease the count of a counter by 1."""
    db = Database()
    # Get the current count of the counter
    result = db.get_counter(uuid)
    # Decrease the count by 1
    count = result.count - 1
    result = db.update_counter(uuid, count)
    current_counter = db.get_counter(uuid)

    result_dict = {'uuid': str(UUID(current_counter.uuid.hex)), 'name': current_counter.name, 'count': current_counter.count}
    return JSONResponse(content=result_dict)

@app.get('/counters/list')
def list_counters():
    db = Database()
    result = db.query_multiple("SELECT counter{uuid, name, count}")
    result_dict = []
    for r in result:
        result_dict.append({'uuid': str(UUID(r.uuid.hex)), 'name': r.name, 'count': r.count})
    return JSONResponse(content=result_dict)

@app.post('/counter/update/{uuid}/{count}')
def update_counter(uuid: str, count: int):
    db = Database()
    result = db.update_counter(uuid, count)
    current_counter = db.get_counter(uuid)
    result_dict = {'uuid': str(UUID(current_counter.uuid.hex)), 'name': current_counter.name, 'count': current_counter.count}
    return JSONResponse(content=result_dict)
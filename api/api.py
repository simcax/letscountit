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

@app.post('/counter/create/{name}')
def create_counter(name: str):
    db = Database()
    counter = Counterthing(name=name)
    result = db.create_counter(name)
    uuid = str(UUID((result.uuid.hex)))
    result_dict = {'uuid': f"{uuid}", 'name': f"{result.name}", 'count': f"{result.count}"}
    return JSONResponse(content=result_dict)
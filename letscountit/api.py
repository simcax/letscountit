from fastapi import FastAPI
from letscountit import base

app = FastAPI()


@app.get('/counter/{uuid}')
def get_counter(uuid: str):
    return uuid




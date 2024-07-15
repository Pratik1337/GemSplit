from fastapi import FastAPI

app = FastAPI()
from fastapi import FastAPI, routing
from gemai import router

app = FastAPI()
app.include_router(router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
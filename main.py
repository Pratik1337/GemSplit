from fastapi import FastAPI, routing
from gemai import router
app = FastAPI()
app.include_router(router)


@app.get("/hello/gemsplit")
def read_root():
    return {"message": "Lets GoooooO!"}
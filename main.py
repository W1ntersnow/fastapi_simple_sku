from fastapi import FastAPI, Request, Response
from api.v1 import item, item_type

from db import engine, models, SessionLocal


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="WarehouseStocksControl",
    version='0.0.1'
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get('/')
def index():
    return {'status': 'Ok!'}


app.include_router(
    item_type.router,
    prefix='/v1/item_type',
    tags=["ItemType"]
)

app.include_router(
    item.router,
    prefix='/v1/item',
    tags=["Item"]
)


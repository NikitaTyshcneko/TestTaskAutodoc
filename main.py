from fastapi import FastAPI

from app.database import db
from app.routers import router

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

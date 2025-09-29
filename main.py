from fastapi import FastAPI
from src.routers import user
from db import create_all_tables

app = FastAPI(lifespan=create_all_tables)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"Hello": "World"}
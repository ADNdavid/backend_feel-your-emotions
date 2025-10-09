from fastapi import FastAPI
from src.routers import user, survey
from db import create_all_tables

app = FastAPI(lifespan=create_all_tables)
app.include_router(user.router)
app.include_router(survey.router)

@app.get("/")
async def root():
    return {"Hello": "Bienvenido a la API de Feel Your Emotions"}
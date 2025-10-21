from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import user, survey, visualizations
from db import create_all_tables
from src.utils.demo_info import DemoGenerator

#origins = [
#    "http://localhost",
#    "http://localhost:5500"
#]
origins = ["*"]

# Crear la aplicación FastAPI
app = FastAPI(lifespan=create_all_tables)
app.include_router(user.router)
app.include_router(survey.router)
app.include_router(visualizations.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"Hello": "Bienvenido a la API de Feel Your Emotions"}
from fastapi import FastAPI
from src.routers import user, survey
from db import create_all_tables
from src.utils.demo_info import DemoGenerator

# Crear el generador
#demo = DemoGenerator()
# Generar datos de prueba
#demo.generate_demo_data()

# Crear la aplicación FastAPI
app = FastAPI(lifespan=create_all_tables)
app.include_router(user.router)
app.include_router(survey.router)

@app.get("/")
async def root():
    return {"Hello": "Bienvenido a la API de Feel Your Emotions"}
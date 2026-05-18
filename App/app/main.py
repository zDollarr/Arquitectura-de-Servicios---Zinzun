from fastapi import FastAPI
from app.routes.carrera_routes import router as carrera_router

app = FastAPI(
    title="API Gestión de Eventos y Actividades",
    version="1.0.0"
)

app.include_router(carrera_router)


@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
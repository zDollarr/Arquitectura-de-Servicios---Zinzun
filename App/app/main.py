from fastapi import FastAPI
from app.routes.evento_routes import router as evento_router
from app.routes.inscripcion_routes import router as inscripcion_router

app = FastAPI(
    title="API Gestión de Eventos y Actividades",
    version="1.0.0"
)

app.include_router(evento_router)
app.include_router(inscripcion_router)


@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
from fastapi import FastAPI
from app.routes.carrera_routes import router as carrera_router
from app.routes.alumno_routes import router as alumno_router
from app.routes.grupo_routes import router as grupo_router
from app.db.mongo import get_database
from app.services.carrera_service import CarreraService

from app.routes.actividad_routes import router as actividad_router

from app.routes.alumno_routes import router as alumno_router
from app.routes.grupo_routes import router as grupo_router
from app.db.mongo import get_database
from app.services.carrera_service import CarreraService
from app.routes.evento_routes import router as evento_router
from app.routes.inscripcion_routes import router as inscripcion_router


app = FastAPI(
    title="API Gestión de Eventos y Actividades",
    version="1.0.0"
)


app.include_router(actividad_router)
app.include_router(carrera_router)
app.include_router(evento_router)
app.include_router(inscripcion_router) 
app.include_router(alumno_router)
app.include_router(grupo_router)


@app.on_event("startup")
async def startup_event():
    db = get_database()
    service = CarreraService(db)
    await service.crear_indice_nombre()


@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
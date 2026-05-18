from typing import Optional
from fastapi import APIRouter
from app.models.actividad_model import ActividadCreate, ActividadUpdate
from app.services.actividad_service import ActividadService


router = APIRouter(
    prefix="/actividades",
    tags=["Actividades"]
)

service = ActividadService()


@router.post("")
def crear_actividad(actividad: ActividadCreate):
    return service.crear_actividad(actividad)


@router.get("")
def consultar_actividades(idEvento: Optional[str] = None, estatus: Optional[bool] = None):
    return service.consultar_actividades(idEvento, estatus)


@router.get("/{idActividad}")
def consultar_actividad_por_id(idActividad: str):
    return service.consultar_actividad_por_id(idActividad)


@router.put("/{idActividad}")
def actualizar_actividad(idActividad: str, actividad: ActividadUpdate):
    return service.actualizar_actividad(idActividad, actividad)


@router.delete("/{idActividad}")
def eliminar_actividad(idActividad: str):
    return service.eliminar_actividad(idActividad)
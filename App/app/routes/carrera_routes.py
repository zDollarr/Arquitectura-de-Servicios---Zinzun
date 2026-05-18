from typing import Optional
from fastapi import APIRouter
from app.models.carrera_model import CarreraCreate, CarreraUpdate
from app.services.carrera_service import CarreraService


router = APIRouter(
    prefix="/carreras",
    tags=["Carreras"]
)

service = CarreraService()


@router.post("")
def crear_carrera(carrera: CarreraCreate):
    return service.crear_carrera(carrera)


@router.get("")
def consultar_carreras(estatus: Optional[bool] = None):
    return service.consultar_carreras(estatus)


@router.get("/{idCarrera}")
def consultar_carrera_por_id(idCarrera: str):
    return service.consultar_carrera_por_id(idCarrera)


@router.put("/{idCarrera}")
def actualizar_carrera(idCarrera: str, carrera: CarreraUpdate):
    return service.actualizar_carrera(idCarrera, carrera)


@router.patch("/{idCarrera}/activar")
def activar_carrera(idCarrera: str):
    return service.activar_carrera(idCarrera)


@router.patch("/{idCarrera}/desactivar")
def desactivar_carrera(idCarrera: str):
    return service.desactivar_carrera(idCarrera)


@router.delete("/{idCarrera}")
def eliminar_carrera(idCarrera: str):
    return service.eliminar_carrera(idCarrera)
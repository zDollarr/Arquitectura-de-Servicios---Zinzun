from typing import Optional
from fastapi import APIRouter, Depends
from app.models.carrera_model import CarreraCreate, CarreraUpdate
from app.services.carrera_service import CarreraService
from app.db.mongo import get_database


router = APIRouter(
    prefix="/carreras",
    tags=["Carreras"]
)


@router.post("")
def crear_carrera(carrera: CarreraCreate, db=Depends(get_database)):
    service = CarreraService(db)
    return service.crear_carrera(carrera)


@router.get("")
def consultar_carreras(estatus: Optional[bool] = None, db=Depends(get_database)):
    service = CarreraService(db)
    return service.consultar_carreras(estatus)


@router.get("/{idCarrera}")
def consultar_carrera_por_id(idCarrera: str, db=Depends(get_database)):
    service = CarreraService(db)
    return service.consultar_carrera_por_id(idCarrera)


@router.put("/{idCarrera}")
def actualizar_carrera(idCarrera: str, carrera: CarreraUpdate, db=Depends(get_database)):
    service = CarreraService(db)
    return service.actualizar_carrera(idCarrera, carrera)


@router.patch("/{idCarrera}/activar")
def activar_carrera(idCarrera: str, db=Depends(get_database)):
    service = CarreraService(db)
    return service.activar_carrera(idCarrera)


@router.patch("/{idCarrera}/desactivar")
def desactivar_carrera(idCarrera: str, db=Depends(get_database)):
    service = CarreraService(db)
    return service.desactivar_carrera(idCarrera)


@router.delete("/{idCarrera}")
def eliminar_carrera(idCarrera: str, db=Depends(get_database)):
    service = CarreraService(db)
    return service.eliminar_carrera(idCarrera)
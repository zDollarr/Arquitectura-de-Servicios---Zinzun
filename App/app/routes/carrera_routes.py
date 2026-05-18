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
async def crear_carrera(carrera: CarreraCreate, db=Depends(get_database)):
    service = CarreraService(db)
    return await service.crear_carrera(carrera)


@router.get("")
async def consultar_carreras(estatus: Optional[bool] = None, db=Depends(get_database)):
    service = CarreraService(db)
    return await service.consultar_carreras(estatus)


@router.get("/{idCarrera}")
async def consultar_carrera_por_id(idCarrera: str, db=Depends(get_database)):
    service = CarreraService(db)
    return await service.consultar_carrera_por_id(idCarrera)


@router.put("/{idCarrera}")
async def actualizar_carrera(idCarrera: str, carrera: CarreraUpdate, db=Depends(get_database)):
    service = CarreraService(db)
    return await service.actualizar_carrera(idCarrera, carrera)


@router.patch("/{idCarrera}/activar")
async def activar_carrera(idCarrera: str, db=Depends(get_database)):
    service = CarreraService(db)
    return await service.activar_carrera(idCarrera)


@router.patch("/{idCarrera}/desactivar")
async def desactivar_carrera(idCarrera: str, db=Depends(get_database)):
    service = CarreraService(db)
    return await service.desactivar_carrera(idCarrera)


@router.delete("/{idCarrera}")
async def eliminar_carrera(idCarrera: str, db=Depends(get_database)):
    service = CarreraService(db)
    return await service.eliminar_carrera(idCarrera)
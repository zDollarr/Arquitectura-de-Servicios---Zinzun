from typing import Optional
from fastapi import APIRouter, Depends, Request
from app.models.carrera_model import CarreraCreate, CarreraUpdate
from app.services.carrera_service import CarreraService
from app.db.mongo import get_database
from app.utils.security import require_roles
from app.core.rate_limit import limiter


router = APIRouter(
    prefix="/carreras",
    tags=["Carreras"]
)


@router.post("")
@limiter.limit("10/minute")
def crear_carrera(
    request: Request,
    carrera: CarreraCreate,
    db=Depends(get_database),
    user: dict = Depends(require_roles(["admin"]))
):
    service = CarreraService(db)
    return service.crear_carrera(carrera)


@router.get("")
@limiter.limit("20/minute")
def consultar_carreras(
    request: Request,
    estatus: Optional[bool] = None,
    db=Depends(get_database),
    user: dict = Depends(require_roles(["admin"]))
):
    service = CarreraService(db)
    return service.consultar_carreras(estatus)


@router.get("/{idCarrera}")
@limiter.limit("20/minute")
def consultar_carrera_por_id(
    request: Request,
    idCarrera: str,
    db=Depends(get_database),
    user: dict = Depends(require_roles(["admin"]))
):
    service = CarreraService(db)
    return service.consultar_carrera_por_id(idCarrera)


@router.put("/{idCarrera}")
@limiter.limit("10/minute")
def actualizar_carrera(
    request: Request,
    idCarrera: str,
    carrera: CarreraUpdate,
    db=Depends(get_database),
    user: dict = Depends(require_roles(["admin"]))
):
    service = CarreraService(db)
    return service.actualizar_carrera(idCarrera, carrera)


@router.patch("/{idCarrera}/activar")
@limiter.limit("10/minute")
def activar_carrera(
    request: Request,
    idCarrera: str,
    db=Depends(get_database),
    user: dict = Depends(require_roles(["admin"]))
):
    service = CarreraService(db)
    return service.activar_carrera(idCarrera)


@router.patch("/{idCarrera}/desactivar")
@limiter.limit("10/minute")
def desactivar_carrera(
    request: Request,
    idCarrera: str,
    db=Depends(get_database),
    user: dict = Depends(require_roles(["admin"]))
):
    service = CarreraService(db)
    return service.desactivar_carrera(idCarrera)


@router.delete("/{idCarrera}")
@limiter.limit("10/minute")
def eliminar_carrera(
    request: Request,
    idCarrera: str,
    db=Depends(get_database),
    user: dict = Depends(require_roles(["admin"]))
):
    service = CarreraService(db)
    return service.eliminar_carrera(idCarrera)
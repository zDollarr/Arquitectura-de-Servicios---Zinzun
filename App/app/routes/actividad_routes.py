from typing import Optional
from fastapi import APIRouter, Depends, Request
from app.models.actividad_model import ActividadCreate, ActividadUpdate
from app.services.actividad_service import ActividadService
from app.utils.security import require_roles
from app.core.rate_limit import limiter


router = APIRouter(
    prefix="/actividades",
    tags=["Actividades"]
)

service = ActividadService()


@router.post("")
@limiter.limit("10/minute")
def crear_actividad(
    request: Request,
    actividad: ActividadCreate,
    user: dict = Depends(require_roles(["organizador"]))
):
    return service.crear_actividad(actividad)


@router.get("")
@limiter.limit("30/minute")
def consultar_actividades(
    request: Request,
    idEvento: Optional[str] = None,
    estatus: Optional[bool] = None
):
    return service.consultar_actividades(idEvento, estatus)


@router.get("/{idActividad}")
@limiter.limit("30/minute")
def consultar_actividad_por_id(
    request: Request,
    idActividad: str
):
    return service.consultar_actividad_por_id(idActividad)


@router.put("/{idActividad}")
@limiter.limit("10/minute")
def actualizar_actividad(
    request: Request,
    idActividad: str,
    actividad: ActividadUpdate,
    user: dict = Depends(require_roles(["organizador"]))
):
    return service.actualizar_actividad(idActividad, actividad)


@router.delete("/{idActividad}")
@limiter.limit("10/minute")
def eliminar_actividad(
    request: Request,
    idActividad: str,
    user: dict = Depends(require_roles(["organizador"]))
):
    return service.eliminar_actividad(idActividad)
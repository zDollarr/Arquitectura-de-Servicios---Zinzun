from fastapi import APIRouter, Depends, Request
from app.models.evento_model import EventoCreate, EventoUpdate
from app.services.evento_service import (
    crear_evento_service,
    consultar_eventos_service,
    consultar_evento_por_id_service,
    actualizar_evento_service,
    cancelar_evento_service
)
from app.utils.security import require_roles
from app.core.rate_limit import limiter

router = APIRouter(prefix="/eventos", tags=["Eventos"])


@router.post("/")
@limiter.limit("10/minute")
def crear_evento(
    request: Request,
    datos: EventoCreate,
    user: dict = Depends(require_roles(["organizador", "admin"]))
):
    return crear_evento_service(datos)


@router.get("/")
@limiter.limit("30/minute")
def consultar_eventos(request: Request):
    return consultar_eventos_service()


@router.get("/{idEvento}")
@limiter.limit("30/minute")
def consultar_evento_por_id(
    request: Request,
    idEvento: str
):
    return consultar_evento_por_id_service(idEvento)


@router.put("/{idEvento}")
@limiter.limit("10/minute")
def actualizar_evento(
    request: Request,
    idEvento: str,
    datos: EventoUpdate,
    user: dict = Depends(require_roles(["organizador", "admin"]))
):
    return actualizar_evento_service(idEvento, datos)


@router.patch("/{idEvento}/cancelar")
@limiter.limit("10/minute")
def cancelar_evento(
    request: Request,
    idEvento: str,
    user: dict = Depends(require_roles(["organizador", "admin"]))
):
    return cancelar_evento_service(idEvento)
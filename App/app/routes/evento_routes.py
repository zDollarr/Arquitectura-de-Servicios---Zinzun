from fastapi import APIRouter
from app.models.evento_model import EventoCreate, EventoUpdate
from app.services.evento_service import (
    crear_evento_service,
    consultar_eventos_service,
    consultar_evento_por_id_service,
    actualizar_evento_service,
    cancelar_evento_service
)

router = APIRouter(prefix="/eventos", tags=["Eventos"])


@router.post("/")
def crear_evento(datos: EventoCreate):
    return crear_evento_service(datos)


@router.get("/")
def consultar_eventos():
    return consultar_eventos_service()


@router.get("/{idEvento}")
def consultar_evento_por_id(idEvento: str):
    return consultar_evento_por_id_service(idEvento)


@router.put("/{idEvento}")
def actualizar_evento(idEvento: str, datos: EventoUpdate):
    return actualizar_evento_service(idEvento, datos)


@router.patch("/{idEvento}/cancelar")
def cancelar_evento(idEvento: str):
    return cancelar_evento_service(idEvento)
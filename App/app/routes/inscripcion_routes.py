from fastapi import APIRouter, Query
from typing import Optional
from app.models.inscripcion_model import InscripcionCreate
from app.services.inscripcion_service import (
    crear_inscripcion_service,
    consultar_inscripciones_service,
    consultar_inscripcion_por_id_service,
    cancelar_inscripcion_service
)

router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])


@router.post("/")
def crear_inscripcion(datos: InscripcionCreate):
    return crear_inscripcion_service(datos)


@router.get("/")
def consultar_inscripciones(
    idAlumno: Optional[str] = Query(None),
    idEvento: Optional[str] = Query(None)
):
    return consultar_inscripciones_service(idAlumno, idEvento)


@router.get("/{idInscripcion}")
def consultar_inscripcion_por_id(idInscripcion: str):
    return consultar_inscripcion_por_id_service(idInscripcion)


@router.delete("/{idInscripcion}")
def cancelar_inscripcion(idInscripcion: str):
    return cancelar_inscripcion_service(idInscripcion)
from fastapi import APIRouter, Query, Depends, Request
from typing import Optional
from app.models.inscripcion_model import InscripcionCreate
from app.services.inscripcion_service import (
    crear_inscripcion_service,
    consultar_inscripciones_service,
    consultar_inscripcion_por_id_service,
    cancelar_inscripcion_service
)
from app.utils.security import require_roles
from app.core.rate_limit import limiter


router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])


@router.post("/")
@limiter.limit("10/minute")
def crear_inscripcion(
    request: Request,
    datos: InscripcionCreate,
    user: dict = Depends(require_roles(["alumno"]))
):
    return crear_inscripcion_service(datos)


@router.get("/")
@limiter.limit("20/minute")
def consultar_inscripciones(
    request: Request,
    idAlumno: Optional[str] = Query(None),
    idEvento: Optional[str] = Query(None),
    user: dict = Depends(require_roles(["admin"]))
):
    return consultar_inscripciones_service(idAlumno, idEvento)


@router.get("/{idInscripcion}")
@limiter.limit("20/minute")
def consultar_inscripcion_por_id(
    request: Request,
    idInscripcion: str,
    user: dict = Depends(require_roles(["admin"]))
):
    return consultar_inscripcion_por_id_service(idInscripcion)


@router.delete("/{idInscripcion}")
@limiter.limit("10/minute")
def cancelar_inscripcion(
    request: Request,
    idInscripcion: str,
    user: dict = Depends(require_roles(["alumno"]))
):
    return cancelar_inscripcion_service(idInscripcion)
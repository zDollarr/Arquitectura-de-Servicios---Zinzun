from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query, Response, status

from app.db.mongo import get_database
from app.models.alumno_model import (
    AlumnoCreate,
    AlumnoCreateResponse,
    AlumnoLogin,
    AlumnoLoginResponse,
    AlumnoOut,
    AlumnosListResponse,
    OperacionResponse,
)
from app.services.alumno_service import (
    activate_alumno,
    authenticate_alumno,
    create_alumno,
    deactivate_alumno,
    delete_alumno,
    get_alumno_by_id,
    list_alumnos,
)


router = APIRouter(prefix="/alumnos", tags=["Alumnos"])


@router.post("", response_model=AlumnoCreateResponse, status_code=status.HTTP_201_CREATED, summary="Crear alumno")
def crear_alumno(
    payload: AlumnoCreate,
    db=Depends(get_database),
) -> AlumnoCreateResponse:
    return create_alumno(db, payload)


@router.post("/login", response_model=AlumnoLoginResponse, summary="Autenticar alumno")
def login_alumno(
    payload: AlumnoLogin,
    db=Depends(get_database),
) -> AlumnoLoginResponse:
    return authenticate_alumno(db, payload)


@router.get("", response_model=AlumnosListResponse, summary="Consultar alumnos")
def consultar_alumnos(
    estatus: Optional[bool] = Query(default=None),
    idCarrera: Optional[str] = Query(default=None, min_length=24, max_length=24),
    idGrupo: Optional[str] = Query(default=None, min_length=24, max_length=24),
    db=Depends(get_database),
) -> AlumnosListResponse:
    return list_alumnos(db, estatus=estatus, id_carrera=idCarrera, id_grupo=idGrupo)


@router.get("/{idAlumno}", response_model=AlumnoOut, summary="Consultar alumno por id")
def consultar_alumno_por_id(
    idAlumno: str,
    db=Depends(get_database),
) -> AlumnoOut:
    return get_alumno_by_id(db, idAlumno)


@router.patch("/{idAlumno}/activar", response_model=OperacionResponse, summary="Activar alumno")
def activar_alumno(
    idAlumno: str,
    db=Depends(get_database),
) -> OperacionResponse:
    return activate_alumno(db, idAlumno)


@router.patch("/{idAlumno}/desactivar", response_model=OperacionResponse, summary="Desactivar alumno")
def desactivar_alumno(
    idAlumno: str,
    db=Depends(get_database),
) -> OperacionResponse:
    return deactivate_alumno(db, idAlumno)


@router.delete("/{idAlumno}", response_model=OperacionResponse, summary="Eliminar alumno")
def eliminar_alumno(
    idAlumno: str,
    db=Depends(get_database),
) -> OperacionResponse:
    return delete_alumno(db, idAlumno)
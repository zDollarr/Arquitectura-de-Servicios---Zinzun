from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query, Response, status
from motor.motor_asyncio import AsyncIOMotorDatabase

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
async def crear_alumno(
    payload: AlumnoCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> AlumnoCreateResponse:
    return await create_alumno(db, payload)


@router.post("/login", response_model=AlumnoLoginResponse, summary="Autenticar alumno")
async def login_alumno(
    payload: AlumnoLogin,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> AlumnoLoginResponse:
    return await authenticate_alumno(db, payload)


@router.get("", response_model=AlumnosListResponse, summary="Consultar alumnos")
async def consultar_alumnos(
    estatus: Optional[bool] = Query(default=None),
    idCarrera: Optional[str] = Query(default=None, min_length=24, max_length=24),
    idGrupo: Optional[str] = Query(default=None, min_length=24, max_length=24),
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> AlumnosListResponse:
    return await list_alumnos(db, estatus=estatus, id_carrera=idCarrera, id_grupo=idGrupo)


@router.get("/{idAlumno}", response_model=AlumnoOut, summary="Consultar alumno por id")
async def consultar_alumno_por_id(
    idAlumno: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> AlumnoOut:
    return await get_alumno_by_id(db, idAlumno)


@router.patch("/{idAlumno}/activar", response_model=OperacionResponse, summary="Activar alumno")
async def activar_alumno(
    idAlumno: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> OperacionResponse:
    return await activate_alumno(db, idAlumno)


@router.patch("/{idAlumno}/desactivar", response_model=OperacionResponse, summary="Desactivar alumno")
async def desactivar_alumno(
    idAlumno: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> OperacionResponse:
    return await deactivate_alumno(db, idAlumno)


@router.delete("/{idAlumno}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar alumno")
async def eliminar_alumno(
    idAlumno: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> Response:
    await delete_alumno(db, idAlumno)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

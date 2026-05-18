from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query, Response, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongo import get_database
from app.models.grupo_model import (
    GrupoCreate,
    GrupoCreateResponse,
    GrupoOut,
    GruposListResponse,
    GrupoUpdate,
    OperacionResponse,
)
from app.services.grupo_service import (
    activate_grupo,
    create_grupo,
    deactivate_grupo,
    delete_grupo,
    get_grupo_by_id,
    list_grupos,
    update_grupo,
)


router = APIRouter(prefix="/grupos", tags=["Grupos"])


@router.post("", response_model=GrupoCreateResponse, status_code=status.HTTP_201_CREATED, summary="Crear grupo")
async def crear_grupo(
    payload: GrupoCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> GrupoCreateResponse:
    return await create_grupo(db, payload)


@router.get("", response_model=GruposListResponse, summary="Consultar grupos")
async def consultar_grupos(
    idCarrera: Optional[str] = Query(default=None, min_length=24, max_length=24),
    semestre: Optional[int] = Query(default=None, gt=0),
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> GruposListResponse:
    return await list_grupos(db, id_carrera=idCarrera, semestre=semestre)


@router.get("/{idGrupo}", response_model=GrupoOut, summary="Consultar grupo por id")
async def consultar_grupo_por_id(
    idGrupo: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> GrupoOut:
    return await get_grupo_by_id(db, idGrupo)


@router.put("/{idGrupo}", response_model=OperacionResponse, summary="Actualizar grupo")
async def actualizar_grupo(
    idGrupo: str,
    payload: GrupoUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> OperacionResponse:
    return await update_grupo(db, idGrupo, payload)


@router.patch("/{idGrupo}/activar", response_model=OperacionResponse, summary="Activar grupo")
async def activar_grupo(
    idGrupo: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> OperacionResponse:
    return await activate_grupo(db, idGrupo)


@router.patch("/{idGrupo}/desactivar", response_model=OperacionResponse, summary="Desactivar grupo")
async def desactivar_grupo(
    idGrupo: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> OperacionResponse:
    return await deactivate_grupo(db, idGrupo)


@router.delete("/{idGrupo}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar grupo")
async def eliminar_grupo(
    idGrupo: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> Response:
    await delete_grupo(db, idGrupo)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

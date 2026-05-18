from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query, Response, status

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
def crear_grupo(
    payload: GrupoCreate,
    db=Depends(get_database),
) -> GrupoCreateResponse:
    return create_grupo(db, payload)


@router.get("", response_model=GruposListResponse, summary="Consultar grupos")
def consultar_grupos(
    idCarrera: Optional[str] = Query(default=None, min_length=24, max_length=24),
    semestre: Optional[int] = Query(default=None, gt=0),
    db=Depends(get_database),
) -> GruposListResponse:
    return list_grupos(db, id_carrera=idCarrera, semestre=semestre)


@router.get("/{idGrupo}", response_model=GrupoOut, summary="Consultar grupo por id")
def consultar_grupo_por_id(
    idGrupo: str,
    db=Depends(get_database),
) -> GrupoOut:
    return get_grupo_by_id(db, idGrupo)


@router.put("/{idGrupo}", response_model=OperacionResponse, summary="Actualizar grupo")
def actualizar_grupo(
    idGrupo: str,
    payload: GrupoUpdate,
    db=Depends(get_database),
) -> OperacionResponse:
    return update_grupo(db, idGrupo, payload)


@router.patch("/{idGrupo}/activar", response_model=OperacionResponse, summary="Activar grupo")
def activar_grupo(
    idGrupo: str,
    db=Depends(get_database),
) -> OperacionResponse:
    return activate_grupo(db, idGrupo)


@router.patch("/{idGrupo}/desactivar", response_model=OperacionResponse, summary="Desactivar grupo")
def desactivar_grupo(
    idGrupo: str,
    db=Depends(get_database),
) -> OperacionResponse:
    return deactivate_grupo(db, idGrupo)


@router.delete("/{idGrupo}", response_model=OperacionResponse, summary="Eliminar grupo")
def eliminar_grupo(
    idGrupo: str,
    db=Depends(get_database),
) -> OperacionResponse:
    return delete_grupo(db, idGrupo)
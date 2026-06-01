from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, status

from app.core.rate_limit import limiter
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
from app.utils.security import require_roles


router = APIRouter(prefix="/grupos", tags=["Grupos"])


@router.post("", response_model=GrupoCreateResponse, status_code=status.HTTP_201_CREATED, summary="Crear grupo")
@limiter.limit("10/minute")
def crear_grupo(
    request: Request,
    payload: GrupoCreate,
    db=Depends(get_database),
    user: dict = Depends(require_roles(["admin"]))
) -> GrupoCreateResponse:
    return create_grupo(db, payload)


@router.get("", response_model=GruposListResponse, summary="Consultar grupos")
@limiter.limit("20/minute")
def consultar_grupos(
    request: Request,
    idCarrera: Optional[str] = Query(default=None, min_length=24, max_length=24),
    semestre: Optional[int] = Query(default=None, gt=0),
    db=Depends(get_database),
    user: dict = Depends(require_roles(["admin"]))
) -> GruposListResponse:
    return list_grupos(db, id_carrera=idCarrera, semestre=semestre)


@router.get("/{idGrupo}", response_model=GrupoOut, summary="Consultar grupo por id")
@limiter.limit("20/minute")
def consultar_grupo_por_id(
    request: Request,
    idGrupo: str,
    db=Depends(get_database),
    user: dict = Depends(require_roles(["admin"]))
) -> GrupoOut:
    return get_grupo_by_id(db, idGrupo)


@router.put("/{idGrupo}", response_model=OperacionResponse, summary="Actualizar grupo")
@limiter.limit("10/minute")
def actualizar_grupo(
    request: Request,
    idGrupo: str,
    payload: GrupoUpdate,
    db=Depends(get_database),
    user: dict = Depends(require_roles(["admin"]))
) -> OperacionResponse:
    return update_grupo(db, idGrupo, payload)


@router.patch("/{idGrupo}/activar", response_model=OperacionResponse, summary="Activar grupo")
@limiter.limit("10/minute")
def activar_grupo(
    request: Request,
    idGrupo: str,
    db=Depends(get_database),
    user: dict = Depends(require_roles(["admin"]))
) -> OperacionResponse:
    return activate_grupo(db, idGrupo)


@router.patch("/{idGrupo}/desactivar", response_model=OperacionResponse, summary="Desactivar grupo")
@limiter.limit("10/minute")
def desactivar_grupo(
    request: Request,
    idGrupo: str,
    db=Depends(get_database),
    user: dict = Depends(require_roles(["admin"]))
) -> OperacionResponse:
    return deactivate_grupo(db, idGrupo)


@router.delete("/{idGrupo}", response_model=OperacionResponse, summary="Eliminar grupo")
@limiter.limit("10/minute")
def eliminar_grupo(
    request: Request,
    idGrupo: str,
    db=Depends(get_database),
    user: dict = Depends(require_roles(["admin"]))
) -> OperacionResponse:
    return delete_grupo(db, idGrupo)
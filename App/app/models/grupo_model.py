from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class GrupoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    idCarrera: str = Field(..., min_length=24, max_length=24)
    semestre: int = Field(..., gt=0)


class GrupoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    idCarrera: Optional[str] = Field(default=None, min_length=24, max_length=24)
    semestre: Optional[int] = Field(default=None, gt=0)
    estatus: Optional[bool] = None


class OperacionResponse(BaseModel):
    codigo: int
    mensaje: str


class GrupoCreateResponse(OperacionResponse):
    idGrupo: str


class GrupoOut(BaseModel):
    idGrupo: str
    nombre: str
    idCarrera: str
    semestre: int
    estatus: bool
    fechaCreacion: date


class GruposListResponse(OperacionResponse):
    grupos: List[GrupoOut]


class GrupoFilterParams(BaseModel):
    idCarrera: Optional[str] = None
    semestre: Optional[int] = None

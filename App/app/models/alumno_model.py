from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class AlumnoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    email: str = Field(..., min_length=5, max_length=150)
    password: str = Field(..., min_length=6, max_length=128)
    numeroControl: str = Field(..., min_length=1, max_length=30)
    rol: str = Field(default="alumno", min_length=1, max_length=50)
    tipo: str = Field(..., min_length=1, max_length=50)
    semestre: int = Field(..., gt=0)
    idCarrera: str = Field(..., min_length=24, max_length=24)
    idGrupo: str = Field(..., min_length=24, max_length=24)


class AlumnoLogin(BaseModel):
    email: str = Field(..., min_length=5, max_length=150)
    password: str = Field(..., min_length=6, max_length=128)


class OperacionResponse(BaseModel):
    codigo: int
    mensaje: str


class AlumnoCreateResponse(OperacionResponse):
    idAlumno: str


class AlumnoBaseOut(BaseModel):
    idAlumno: str
    nombre: str
    email: str
    numeroControl: str
    rol: str
    tipo: str
    semestre: int
    idCarrera: str
    idGrupo: str
    estatus: bool


class AlumnoOut(AlumnoBaseOut):
    fechaCreacion: date


class AlumnoLoginResponse(OperacionResponse):
    alumno: AlumnoBaseOut


class AlumnosListResponse(OperacionResponse):
    alumnos: List[AlumnoOut]


class AlumnoFilterParams(BaseModel):
    estatus: Optional[bool] = None
    idCarrera: Optional[str] = None
    idGrupo: Optional[str] = None

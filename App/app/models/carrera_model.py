from typing import Optional
from pydantic import BaseModel


class CarreraCreate(BaseModel):
    nombre: str


class CarreraUpdate(BaseModel):
    nombre: Optional[str] = None
    estatus: Optional[bool] = None


class Salida(BaseModel):
    codigo: int
    mensaje: str
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ActividadCreate(BaseModel):
    nombre: str
    descripcion: str
    idEvento: str
    fecha: datetime
    estatus: Optional[bool] = True


class ActividadUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    idEvento: Optional[str] = None
    fecha: Optional[datetime] = None
    estatus: Optional[bool] = None


class Salida(BaseModel):
    codigo: int
    mensaje: str
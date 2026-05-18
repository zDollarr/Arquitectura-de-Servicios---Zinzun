from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventoCreate(BaseModel):
    nombre: str
    fechaInicio: datetime
    capacidadMaxima: int
    descripcion: str
    tipo: str

class EventoResponse(BaseModel):
    idEvento: str
    nombre: str
    fechaInicio: datetime
    capacidadMaxima: int
    inscritos: int
    estatus: str
    descripcion: str
    tipo: str
    fechaRegistro: datetime
    
class EventoUpdate(BaseModel):
    nombre: Optional[str] = None
    fechaInicio: Optional[datetime] = None
    capacidadMaxima: Optional[int] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    estatus: Optional[str] = None
    

from pydantic import BaseModel
from datetime import datetime


class InscripcionCreate(BaseModel):
    idAlumno: str
    idEvento: str
    
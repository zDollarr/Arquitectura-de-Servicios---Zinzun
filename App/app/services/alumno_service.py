from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Dict, List, Optional

from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.alumno_model import (
    AlumnoBaseOut,
    AlumnoCreate,
    AlumnoCreateResponse,
    AlumnoLogin,
    AlumnoLoginResponse,
    AlumnoOut,
    AlumnosListResponse,
    OperacionResponse,
)


ALUMNOS_COLLECTION = "alumnos"
CARRERAS_COLLECTION = "carreras"
GRUPOS_COLLECTION = "grupos"


def _hash_password(password: str) -> str:
    return sha256(password.encode("utf-8")).hexdigest()


def _validate_object_id(value: str, field_name: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El campo {field_name} no tiene un ObjectId válido.",
        )
    return ObjectId(value)


def _serialize_alumno(document: Dict[str, Any]) -> Dict[str, Any]:
    fecha = document.get("fechaCreacion")
    if isinstance(fecha, datetime):
        fecha = fecha.date()

    return {
        "idAlumno": str(document["_id"]),
        "nombre": document["nombre"],
        "email": document["email"],
        "numeroControl": document["numeroControl"],
        "rol": document["rol"],
        "tipo": document["tipo"],
        "semestre": document["semestre"],
        "idCarrera": str(document["idCarrera"]),
        "idGrupo": str(document["idGrupo"]),
        "estatus": document["estatus"],
        "fechaCreacion": fecha,
    }


async def create_alumno(db: AsyncIOMotorDatabase, payload: AlumnoCreate) -> AlumnoCreateResponse:
    alumnos = db[ALUMNOS_COLLECTION]
    carreras = db[CARRERAS_COLLECTION]
    grupos = db[GRUPOS_COLLECTION]

    existing_email = await alumnos.find_one({"email": payload.email.strip().lower()})
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un alumno registrado con ese email.",
        )

    existing_numero_control = await alumnos.find_one({"numeroControl": payload.numeroControl.strip()})
    if existing_numero_control:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un alumno registrado con ese número de control.",
        )

    carrera_id = _validate_object_id(payload.idCarrera, "idCarrera")
    grupo_id = _validate_object_id(payload.idGrupo, "idGrupo")

    carrera = await carreras.find_one({"_id": carrera_id})
    if not carrera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La carrera indicada no existe.",
        )

    grupo = await grupos.find_one({"_id": grupo_id})
    if not grupo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El grupo indicado no existe.",
        )

    document = {
        "nombre": payload.nombre.strip(),
        "email": payload.email.strip().lower(),
        "password": _hash_password(payload.password),
        "numeroControl": payload.numeroControl.strip(),
        "rol": payload.rol.strip(),
        "tipo": payload.tipo.strip(),
        "semestre": payload.semestre,
        "idCarrera": carrera_id,
        "idGrupo": grupo_id,
        "estatus": True,
        "fechaCreacion": datetime.now(timezone.utc),
    }

    result = await alumnos.insert_one(document)

    return AlumnoCreateResponse(
        codigo=status.HTTP_201_CREATED,
        mensaje="Alumno creado correctamente.",
        idAlumno=str(result.inserted_id),
    )


async def authenticate_alumno(db: AsyncIOMotorDatabase, credentials: AlumnoLogin) -> AlumnoLoginResponse:
    alumnos = db[ALUMNOS_COLLECTION]

    alumno = await alumnos.find_one({"email": credentials.email.strip().lower()})
    if not alumno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe un alumno con ese email.",
        )

    if alumno.get("password") != _hash_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La contraseña es incorrecta.",
        )

    if not alumno.get("estatus", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El alumno se encuentra inactivo.",
        )

    serialized = _serialize_alumno(alumno)
    alumno_auth = AlumnoBaseOut(**{k: v for k, v in serialized.items() if k != "fechaCreacion"})

    return AlumnoLoginResponse(
        codigo=status.HTTP_200_OK,
        mensaje="Autenticación correcta.",
        alumno=alumno_auth,
    )


async def delete_alumno(db: AsyncIOMotorDatabase, id_alumno: str) -> None:
    alumnos = db[ALUMNOS_COLLECTION]
    alumno_id = _validate_object_id(id_alumno, "idAlumno")

    result = await alumnos.delete_one({"_id": alumno_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El alumno indicado no existe.",
        )


async def activate_alumno(db: AsyncIOMotorDatabase, id_alumno: str) -> OperacionResponse:
    return await _update_alumno_status(db, id_alumno, True, "Alumno activado correctamente.")


async def deactivate_alumno(db: AsyncIOMotorDatabase, id_alumno: str) -> OperacionResponse:
    return await _update_alumno_status(db, id_alumno, False, "Alumno desactivado correctamente.")


async def _update_alumno_status(
    db: AsyncIOMotorDatabase,
    id_alumno: str,
    new_status: bool,
    success_message: str,
) -> OperacionResponse:
    alumnos = db[ALUMNOS_COLLECTION]
    alumno_id = _validate_object_id(id_alumno, "idAlumno")

    result = await alumnos.update_one({"_id": alumno_id}, {"$set": {"estatus": new_status}})
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El alumno indicado no existe.",
        )

    return OperacionResponse(codigo=status.HTTP_200_OK, mensaje=success_message)


async def get_alumno_by_id(db: AsyncIOMotorDatabase, id_alumno: str) -> AlumnoOut:
    alumnos = db[ALUMNOS_COLLECTION]
    alumno_id = _validate_object_id(id_alumno, "idAlumno")

    alumno = await alumnos.find_one({"_id": alumno_id})
    if not alumno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El alumno indicado no existe.",
        )

    return AlumnoOut(**_serialize_alumno(alumno))


async def list_alumnos(
    db: AsyncIOMotorDatabase,
    estatus: Optional[bool] = None,
    id_carrera: Optional[str] = None,
    id_grupo: Optional[str] = None,
) -> AlumnosListResponse:
    alumnos = db[ALUMNOS_COLLECTION]
    query: Dict[str, Any] = {}

    if estatus is not None:
        query["estatus"] = estatus
    if id_carrera is not None:
        query["idCarrera"] = _validate_object_id(id_carrera, "idCarrera")
    if id_grupo is not None:
        query["idGrupo"] = _validate_object_id(id_grupo, "idGrupo")

    documents = await alumnos.find(query).sort("fechaCreacion", -1).to_list(length=None)
    serialized: List[AlumnoOut] = [AlumnoOut(**_serialize_alumno(doc)) for doc in documents]

    mensaje = "Consulta de alumnos realizada correctamente."
    if estatus is not None and id_carrera is None and id_grupo is None:
        mensaje = f"Consulta de alumnos filtrados por estatus={estatus} realizada correctamente."
    elif id_carrera is not None and estatus is None and id_grupo is None:
        mensaje = "Consulta de alumnos filtrados por carrera realizada correctamente."
    elif id_grupo is not None and estatus is None and id_carrera is None:
        mensaje = "Consulta de alumnos filtrados por grupo realizada correctamente."
    elif query:
        mensaje = "Consulta de alumnos filtrados realizada correctamente."

    return AlumnosListResponse(codigo=status.HTTP_200_OK, mensaje=mensaje, alumnos=serialized)

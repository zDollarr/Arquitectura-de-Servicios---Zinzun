from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from bson import ObjectId
from fastapi import HTTPException, status

from app.models.grupo_model import (
    GrupoCreate,
    GrupoCreateResponse,
    GrupoOut,
    GruposListResponse,
    GrupoUpdate,
    OperacionResponse,
)


GRUPOS_COLLECTION = "grupos"
CARRERAS_COLLECTION = "carreras"


def _validate_object_id(value: str, field_name: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El campo {field_name} no tiene un ObjectId válido.",
        )
    return ObjectId(value)


def _ensure_carrera_exists(db, id_carrera: str) -> ObjectId:
    carrera_id = _validate_object_id(id_carrera, "idCarrera")

    carrera = db[CARRERAS_COLLECTION].find_one({"_id": carrera_id})
    if not carrera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La carrera indicada no existe.",
        )

    return carrera_id


def _serialize_grupo(document: Dict[str, Any]) -> Dict[str, Any]:
    fecha = document.get("fechaCreacion")
    if isinstance(fecha, datetime):
        fecha = fecha.date()

    return {
        "idGrupo": str(document["_id"]),
        "nombre": document["nombre"],
        "idCarrera": str(document["idCarrera"]),
        "semestre": document["semestre"],
        "estatus": document["estatus"],
        "fechaCreacion": fecha,
    }


def create_grupo(db, payload: GrupoCreate) -> GrupoCreateResponse:
    grupos = db[GRUPOS_COLLECTION]
    carrera_id = _ensure_carrera_exists(db, payload.idCarrera)

    document = {
        "nombre": payload.nombre.strip(),
        "idCarrera": carrera_id,
        "semestre": payload.semestre,
        "estatus": True,
        "fechaCreacion": datetime.now(timezone.utc),
    }

    result = grupos.insert_one(document)

    return GrupoCreateResponse(
        codigo=status.HTTP_201_CREATED,
        mensaje="Grupo creado correctamente.",
        idGrupo=str(result.inserted_id),
    )


def update_grupo(db, id_grupo: str, payload: GrupoUpdate) -> OperacionResponse:
    grupos = db[GRUPOS_COLLECTION]
    grupo_id = _validate_object_id(id_grupo, "idGrupo")

    existing = grupos.find_one({"_id": grupo_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El grupo indicado no existe.",
        )

    updates: Dict[str, Any] = {}

    payload_dict = (
        payload.model_dump(exclude_none=True)
        if hasattr(payload, "model_dump")
        else payload.dict(exclude_none=True)
    )

    if "nombre" in payload_dict:
        updates["nombre"] = payload_dict["nombre"].strip()

    if "idCarrera" in payload_dict:
        updates["idCarrera"] = _ensure_carrera_exists(db, payload_dict["idCarrera"])

    if "semestre" in payload_dict:
        updates["semestre"] = payload_dict["semestre"]

    if "estatus" in payload_dict:
        updates["estatus"] = payload_dict["estatus"]

    if not updates:
        return OperacionResponse(
            codigo=status.HTTP_200_OK,
            mensaje="No se enviaron cambios para actualizar el grupo.",
        )

    grupos.update_one({"_id": grupo_id}, {"$set": updates})

    return OperacionResponse(
        codigo=status.HTTP_200_OK,
        mensaje="Grupo actualizado correctamente."
    )


def delete_grupo(db, id_grupo: str) -> OperacionResponse:
    grupos = db[GRUPOS_COLLECTION]
    grupo_id = _validate_object_id(id_grupo, "idGrupo")

    result = grupos.delete_one({"_id": grupo_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El grupo indicado no existe.",
        )

    return OperacionResponse(
        codigo=status.HTTP_200_OK,
        mensaje="Grupo eliminado correctamente."
    )


def activate_grupo(db, id_grupo: str) -> OperacionResponse:
    return _update_grupo_status(
        db,
        id_grupo,
        True,
        "Grupo activado correctamente."
    )


def deactivate_grupo(db, id_grupo: str) -> OperacionResponse:
    return _update_grupo_status(
        db,
        id_grupo,
        False,
        "Grupo desactivado correctamente."
    )


def _update_grupo_status(
    db,
    id_grupo: str,
    new_status: bool,
    success_message: str,
) -> OperacionResponse:
    grupos = db[GRUPOS_COLLECTION]
    grupo_id = _validate_object_id(id_grupo, "idGrupo")

    result = grupos.update_one(
        {"_id": grupo_id},
        {"$set": {"estatus": new_status}}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El grupo indicado no existe.",
        )

    return OperacionResponse(
        codigo=status.HTTP_200_OK,
        mensaje=success_message
    )


def get_grupo_by_id(db, id_grupo: str) -> GrupoOut:
    grupos = db[GRUPOS_COLLECTION]
    grupo_id = _validate_object_id(id_grupo, "idGrupo")

    grupo = grupos.find_one({"_id": grupo_id})

    if not grupo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El grupo indicado no existe.",
        )

    return GrupoOut(**_serialize_grupo(grupo))


def list_grupos(
    db,
    id_carrera: Optional[str] = None,
    semestre: Optional[int] = None,
) -> GruposListResponse:
    grupos = db[GRUPOS_COLLECTION]
    query: Dict[str, Any] = {}

    if id_carrera is not None:
        query["idCarrera"] = _validate_object_id(id_carrera, "idCarrera")

    if semestre is not None:
        query["semestre"] = semestre

    documents = list(grupos.find(query).sort("fechaCreacion", -1))

    serialized: List[GrupoOut] = [
        GrupoOut(**_serialize_grupo(doc)) for doc in documents
    ]

    mensaje = "Consulta de grupos realizada correctamente."

    if id_carrera is not None and semestre is None:
        mensaje = "Consulta de grupos filtrados por carrera realizada correctamente."
    elif semestre is not None and id_carrera is None:
        mensaje = "Consulta de grupos filtrados por semestre realizada correctamente."
    elif query:
        mensaje = "Consulta de grupos filtrados realizada correctamente."

    return GruposListResponse(
        codigo=status.HTTP_200_OK,
        mensaje=mensaje,
        grupos=serialized
    )
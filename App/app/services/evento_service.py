from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime
from app.db.mongo import get_db


def crear_evento_service(datos):
    db = get_db()
    eventos_collection = db["eventos"]

    if datos.capacidadMaxima <= 0:
        raise HTTPException(status_code=400, detail="La capacidad maxima debe ser mayor a 0")

    nuevo_evento = {
        "nombre": datos.nombre,
        "fechaInicio": datos.fechaInicio,
        "capacidadMaxima": datos.capacidadMaxima,
        "inscritos": 0,
        "estatus": "activo",
        "descripcion": datos.descripcion,
        "tipo": datos.tipo,
        "fechaRegistro": datetime.now()
    }

    resultado = eventos_collection.insert_one(nuevo_evento)

    return {
        "codigo": 201,
        "mensaje": "Evento creado correctamente",
        "idEvento": str(resultado.inserted_id)
    }


def consultar_eventos_service():
    db = get_db()
    eventos_collection = db["eventos"]
    eventos_cursor = eventos_collection.find()

    eventos = []
    for evento in eventos_cursor:
        eventos.append({
            "idEvento": str(evento["_id"]),
            "nombre": evento.get("nombre", ""),
            "fechaInicio": evento.get("fechaInicio"),
            "capacidadMaxima": evento.get("capacidadMaxima", 0),
            "inscritos": evento.get("inscritos", 0),
            "estatus": evento.get("estatus", ""),
            "descripcion": evento.get("descripcion", ""),
            "tipo": evento.get("tipo", ""),
            "fechaRegistro": evento.get("fechaRegistro")
        })

    return {
        "codigo": 200,
        "mensaje": "Consulta de eventos exitosa",
        "eventos": eventos
    }


def consultar_evento_por_id_service(idEvento: str):
    db = get_db()
    eventos_collection = db["eventos"]

    if not ObjectId.is_valid(idEvento):
        raise HTTPException(status_code=400, detail="Id de evento no válido")

    evento = eventos_collection.find_one({"_id": ObjectId(idEvento)})

    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    return {
        "idEvento": str(evento["_id"]),
        "nombre": evento.get("nombre", ""),
        "fechaInicio": evento.get("fechaInicio"),
        "capacidadMaxima": evento.get("capacidadMaxima", 0),
        "inscritos": evento.get("inscritos", 0),
        "estatus": evento.get("estatus", ""),
        "descripcion": evento.get("descripcion", ""),
        "tipo": evento.get("tipo", ""),
        "fechaRegistro": evento.get("fechaRegistro")
    }


def actualizar_evento_service(idEvento: str, datos):
    db = get_db()
    eventos_collection = db["eventos"]

    if not ObjectId.is_valid(idEvento):
        raise HTTPException(status_code=400, detail="Id de evento no válido")

    evento_existente = eventos_collection.find_one({"_id": ObjectId(idEvento)})

    if not evento_existente:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    datos_actualizar = datos.dict(exclude_unset=True)

    if "capacidadMaxima" in datos_actualizar and datos_actualizar["capacidadMaxima"] <= 0:
        raise HTTPException(status_code=400, detail="La capacidad maxima debe ser mayor a 0")

    if datos_actualizar:
        eventos_collection.update_one(
            {"_id": ObjectId(idEvento)},
            {"$set": datos_actualizar}
        )

    return {
        "codigo": 200,
        "mensaje": "Evento actualizado correctamente"
    }


def cancelar_evento_service(idEvento: str):
    db = get_db()
    eventos_collection = db["eventos"]

    if not ObjectId.is_valid(idEvento):
        raise HTTPException(status_code=400, detail="Id de evento no válido")

    evento_existente = eventos_collection.find_one({"_id": ObjectId(idEvento)})

    if not evento_existente:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    eventos_collection.update_one(
        {"_id": ObjectId(idEvento)},
        {"$set": {"estatus": "cancelado"}}
    )

    return {
        "codigo": 200,
        "mensaje": "Evento cancelado correctamente"
    }
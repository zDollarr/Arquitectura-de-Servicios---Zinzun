from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime
from app.db.mongo import get_db


def crear_inscripcion_service(datos):
    db = get_db()
    inscripciones_collection = db["inscripciones"]
    alumnos_collection = db["alumnos"]
    eventos_collection = db["eventos"]

    if not ObjectId.is_valid(datos.idAlumno):
        raise HTTPException(status_code=400, detail="Id de alumno no válido")

    if not ObjectId.is_valid(datos.idEvento):
        raise HTTPException(status_code=400, detail="Id de evento no válido")

    alumno_existente = alumnos_collection.find_one({"_id": ObjectId(datos.idAlumno)})
    if not alumno_existente:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    evento_existente = eventos_collection.find_one({"_id": ObjectId(datos.idEvento)})
    if not evento_existente:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    if evento_existente.get("estatus") != "activo":
        raise HTTPException(status_code=400, detail="Solo se permite inscripción en eventos activos")

    inscritos_actuales = evento_existente.get("inscritos", 0)
    capacidad_maxima = evento_existente.get("capacidadMaxima", 0)

    if inscritos_actuales >= capacidad_maxima:
        raise HTTPException(status_code=400, detail="Evento lleno")

    inscripcion_duplicada = inscripciones_collection.find_one({
        "idAlumno": ObjectId(datos.idAlumno),
        "idEvento": ObjectId(datos.idEvento)
    })

    if inscripcion_duplicada:
        raise HTTPException(status_code=400, detail="El alumno ya está inscrito en este evento")

    nueva_inscripcion = {
        "idAlumno": ObjectId(datos.idAlumno),
        "idEvento": ObjectId(datos.idEvento),
        "fechaInscripcion": datetime.now(),
        "asistencia": False
    }

    resultado = inscripciones_collection.insert_one(nueva_inscripcion)

    eventos_collection.update_one(
        {"_id": ObjectId(datos.idEvento)},
        {"$inc": {"inscritos": 1}}
    )

    return {
        "codigo": 201,
        "mensaje": "Inscripción creada correctamente",
        "idInscripcion": str(resultado.inserted_id)
    }


def consultar_inscripciones_service(idAlumno=None, idEvento=None):
    db = get_db()
    inscripciones_collection = db["inscripciones"]

    filtro = {}

    if idAlumno:
        if not ObjectId.is_valid(idAlumno):
            raise HTTPException(status_code=400, detail="Id de alumno no válido")
        filtro["idAlumno"] = ObjectId(idAlumno)

    if idEvento:
        if not ObjectId.is_valid(idEvento):
            raise HTTPException(status_code=400, detail="Id de evento no válido")
        filtro["idEvento"] = ObjectId(idEvento)

    inscripciones_cursor = inscripciones_collection.find(filtro)

    inscripciones = []
    for inscripcion in inscripciones_cursor:
        inscripciones.append({
            "idInscripcion": str(inscripcion["_id"]),
            "idAlumno": str(inscripcion.get("idAlumno", "")),
            "idEvento": str(inscripcion.get("idEvento", "")),
            "fechaInscripcion": inscripcion.get("fechaInscripcion"),
            "asistencia": inscripcion.get("asistencia", False)
        })

    return {
        "codigo": 200,
        "mensaje": "Consulta de inscripciones exitosa",
        "inscripciones": inscripciones
    }


def consultar_inscripcion_por_id_service(idInscripcion: str):
    db = get_db()
    inscripciones_collection = db["inscripciones"]

    if not ObjectId.is_valid(idInscripcion):
        raise HTTPException(status_code=400, detail="Id de inscripción no válido")

    inscripcion = inscripciones_collection.find_one({"_id": ObjectId(idInscripcion)})

    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")

    return {
        "idInscripcion": str(inscripcion["_id"]),
        "idAlumno": str(inscripcion.get("idAlumno", "")),
        "idEvento": str(inscripcion.get("idEvento", "")),
        "fechaInscripcion": inscripcion.get("fechaInscripcion"),
        "asistencia": inscripcion.get("asistencia", False)
    }


def cancelar_inscripcion_service(idInscripcion: str):
    db = get_db()
    inscripciones_collection = db["inscripciones"]
    eventos_collection = db["eventos"]

    if not ObjectId.is_valid(idInscripcion):
        raise HTTPException(status_code=400, detail="Id de inscripción no válido")

    inscripcion = inscripciones_collection.find_one({"_id": ObjectId(idInscripcion)})

    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")

    eventos_collection.update_one(
        {"_id": inscripcion["idEvento"]},
        {"$inc": {"inscritos": -1}}
    )

    inscripciones_collection.delete_one({"_id": ObjectId(idInscripcion)})

    return {
        "codigo": 200,
        "mensaje": "Inscripción cancelada correctamente"
    }
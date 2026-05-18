from bson import ObjectId
from app.db.mongo import db
from app.models.actividad_model import ActividadCreate, ActividadUpdate


class ActividadService:
    def __init__(self):
        self.collection = db["actividades"]
        self.eventos_collection = db["eventos"]

    def convertir_actividad(self, actividad):
        actividad["idActividad"] = str(actividad["_id"])
        del actividad["_id"]

        if "idEvento" in actividad:
            actividad["idEvento"] = str(actividad["idEvento"])

        if "fecha" in actividad:
            actividad["fecha"] = str(actividad["fecha"])

        return actividad

    def validar_evento(self, idEvento: str):
        if not ObjectId.is_valid(idEvento):
            return False

        evento = self.eventos_collection.find_one({"_id": ObjectId(idEvento)})
        return evento is not None

    def crear_actividad(self, actividad: ActividadCreate):
        if not ObjectId.is_valid(actividad.idEvento):
            return {
                "codigo": 400,
                "mensaje": "ID de evento no válido"
            }

        if not self.validar_evento(actividad.idEvento):
            return {
                "codigo": 404,
                "mensaje": "El evento indicado no existe"
            }

        nueva_actividad = {
            "nombre": actividad.nombre,
            "descripcion": actividad.descripcion,
            "idEvento": ObjectId(actividad.idEvento),
            "fecha": actividad.fecha,
            "estatus": actividad.estatus
        }

        resultado = self.collection.insert_one(nueva_actividad)

        return {
            "codigo": 200,
            "mensaje": "Actividad creada correctamente",
            "idActividad": str(resultado.inserted_id)
        }

    def consultar_actividades(self, idEvento: str = None, estatus: bool = None):
        filtro = {}

        if idEvento is not None:
            if not ObjectId.is_valid(idEvento):
                return {
                    "codigo": 400,
                    "mensaje": "ID de evento no válido"
                }

            filtro["idEvento"] = ObjectId(idEvento)

        if estatus is not None:
            filtro["estatus"] = estatus

        actividades = list(self.collection.find(filtro))
        actividades = [self.convertir_actividad(actividad) for actividad in actividades]

        return {
            "codigo": 200,
            "mensaje": "Actividades consultadas correctamente",
            "actividades": actividades
        }

    def consultar_actividad_por_id(self, idActividad: str):
        if not ObjectId.is_valid(idActividad):
            return {
                "codigo": 400,
                "mensaje": "ID de actividad no válido"
            }

        actividad = self.collection.find_one({"_id": ObjectId(idActividad)})

        if actividad is None:
            return {
                "codigo": 404,
                "mensaje": "Actividad no encontrada"
            }

        return self.convertir_actividad(actividad)

    def actualizar_actividad(self, idActividad: str, actividad: ActividadUpdate):
        if not ObjectId.is_valid(idActividad):
            return {
                "codigo": 400,
                "mensaje": "ID de actividad no válido"
            }

        datos_actualizar = actividad.dict(exclude_unset=True)

        if not datos_actualizar:
            return {
                "codigo": 400,
                "mensaje": "No se enviaron datos para actualizar"
            }

        if "idEvento" in datos_actualizar:
            idEvento = datos_actualizar["idEvento"]

            if not ObjectId.is_valid(idEvento):
                return {
                    "codigo": 400,
                    "mensaje": "ID de evento no válido"
                }

            if not self.validar_evento(idEvento):
                return {
                    "codigo": 404,
                    "mensaje": "El evento indicado no existe"
                }

            datos_actualizar["idEvento"] = ObjectId(idEvento)

        resultado = self.collection.update_one(
            {"_id": ObjectId(idActividad)},
            {"$set": datos_actualizar}
        )

        if resultado.matched_count == 0:
            return {
                "codigo": 404,
                "mensaje": "Actividad no encontrada"
            }

        return {
            "codigo": 200,
            "mensaje": "Actividad actualizada correctamente"
        }

    def eliminar_actividad(self, idActividad: str):
        if not ObjectId.is_valid(idActividad):
            return {
                "codigo": 400,
                "mensaje": "ID de actividad no válido"
            }

        resultado = self.collection.delete_one({"_id": ObjectId(idActividad)})

        if resultado.deleted_count == 0:
            return {
                "codigo": 404,
                "mensaje": "Actividad no encontrada"
            }

        return {
            "codigo": 200,
            "mensaje": "Actividad eliminada correctamente"
        }
from datetime import datetime
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.db.mongo import db
from app.models.carrera_model import CarreraCreate, CarreraUpdate


class CarreraService:
    def __init__(self):
        self.collection = db["carreras"]
        self.collection.create_index("nombre", unique=True)

    def convertir_carrera(self, carrera):
        carrera["idCarrera"] = str(carrera["_id"])
        del carrera["_id"]

        if "fechaCreacion" in carrera:
            carrera["fechaCreacion"] = str(carrera["fechaCreacion"])

        return carrera

    def crear_carrera(self, carrera: CarreraCreate):
        try:
            nueva_carrera = {
                "nombre": carrera.nombre,
                "estatus": True,
                "fechaCreacion": datetime.now()
            }

            resultado = self.collection.insert_one(nueva_carrera)

            return {
                "codigo": 200,
                "mensaje": "Carrera creada correctamente",
                "idCarrera": str(resultado.inserted_id)
            }

        except DuplicateKeyError:
            return {
                "codigo": 400,
                "mensaje": "Ya existe una carrera con ese nombre"
            }

        except Exception as error:
            return {
                "codigo": 500,
                "mensaje": f"Error al crear carrera: {str(error)}"
            }

    def consultar_carreras(self, estatus: bool = None):
        filtro = {}

        if estatus is not None:
            filtro["estatus"] = estatus

        carreras = list(self.collection.find(filtro))
        carreras = [self.convertir_carrera(carrera) for carrera in carreras]

        return {
            "codigo": 200,
            "mensaje": "Carreras consultadas correctamente",
            "carreras": carreras
        }

    def consultar_carrera_por_id(self, idCarrera: str):
        if not ObjectId.is_valid(idCarrera):
            return {
                "codigo": 400,
                "mensaje": "ID de carrera no válido"
            }

        carrera = self.collection.find_one({"_id": ObjectId(idCarrera)})

        if carrera is None:
            return {
                "codigo": 404,
                "mensaje": "Carrera no encontrada"
            }

        return self.convertir_carrera(carrera)

    def actualizar_carrera(self, idCarrera: str, carrera: CarreraUpdate):
        if not ObjectId.is_valid(idCarrera):
            return {
                "codigo": 400,
                "mensaje": "ID de carrera no válido"
            }

        datos_actualizar = carrera.dict(exclude_unset=True)

        if not datos_actualizar:
            return {
                "codigo": 400,
                "mensaje": "No se enviaron datos para actualizar"
            }

        try:
            resultado = self.collection.update_one(
                {"_id": ObjectId(idCarrera)},
                {"$set": datos_actualizar}
            )

            if resultado.matched_count == 0:
                return {
                    "codigo": 404,
                    "mensaje": "Carrera no encontrada"
                }

            return {
                "codigo": 200,
                "mensaje": "Carrera actualizada correctamente"
            }

        except DuplicateKeyError:
            return {
                "codigo": 400,
                "mensaje": "Ya existe una carrera con ese nombre"
            }

    def activar_carrera(self, idCarrera: str):
        return self.cambiar_estatus(idCarrera, True)

    def desactivar_carrera(self, idCarrera: str):
        return self.cambiar_estatus(idCarrera, False)

    def cambiar_estatus(self, idCarrera: str, estatus: bool):
        if not ObjectId.is_valid(idCarrera):
            return {
                "codigo": 400,
                "mensaje": "ID de carrera no válido"
            }

        resultado = self.collection.update_one(
            {"_id": ObjectId(idCarrera)},
            {"$set": {"estatus": estatus}}
        )

        if resultado.matched_count == 0:
            return {
                "codigo": 404,
                "mensaje": "Carrera no encontrada"
            }

        return {
            "codigo": 200,
            "mensaje": "Estatus de carrera actualizado correctamente"
        }

    def eliminar_carrera(self, idCarrera: str):
        if not ObjectId.is_valid(idCarrera):
            return {
                "codigo": 400,
                "mensaje": "ID de carrera no válido"
            }

        resultado = self.collection.delete_one({"_id": ObjectId(idCarrera)})

        if resultado.deleted_count == 0:
            return {
                "codigo": 404,
                "mensaje": "Carrera no encontrada"
            }

        return {
            "codigo": 200,
            "mensaje": "Carrera eliminada correctamente"
        }
from fastapi import HTTPException
from app.db.mongo import get_database
from app.utils.security import verify_password, create_access_token

def login_service(datos):
    db = get_database()
    alumnos_collection = db["alumnos"]

    alumno = alumnos_collection.find_one({"email": datos.email})

    if not alumno:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    if not alumno.get("estatus", True):
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    if not verify_password(datos.password, alumno["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token_data = {
        "sub": str(alumno["_id"]),
        "email": alumno["email"],
        "rol": alumno["rol"],
        "nombre": alumno["nombre"]
    }

    access_token = create_access_token(token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "idAlumno": str(alumno["_id"]),
            "nombre": alumno["nombre"],
            "email": alumno["email"],
            "rol": alumno["rol"]
        }
    }
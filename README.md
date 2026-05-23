# Arquitectura de Servicios

Proyecto académico desarrollado en equipo de 3 personas para la materia de Arquitectura de Servicios en el ITESZ. El sistema gestiona alumnos, carreras, grupos, eventos, actividades e inscripciones mediante una API REST construida con FastAPI y MongoDB.

El desarrollo fue coordinado de forma colaborativa a través de GitHub, con responsabilidades documentadas por recurso y avances trazables mediante commits.

---

## Integrantes

- Fernando Santos Gómez
- Francisco Daniel Arciniega Robles
- Angel Ramón Ramírez Mendoza

---

## Recursos del sistema

- Alumno
- Carrera
- Grupo
- Evento
- Actividad
- Inscripción

---

## Responsables por recurso

| Recurso | Responsable |
|---|---|
| Alumno | Francisco Daniel Arciniega Robles |
| Carrera | Angel Ramón Ramírez Mendoza |
| Grupo | Francisco Daniel Arciniega Robles |
| Evento | Fernando Santos Gómez |
| Actividad | Angel Ramón Ramírez Mendoza |
| Inscripción | Fernando Santos Gómez |

---

## Tech Stack

FastAPI · Python · MongoDB · REST API · Uvicorn

---

## Estructura del Repositorio

```text
Documentacion/   # Definición del proyecto, modelo de dominio, diagrama de clases y servicios REST
BD/              # Diagrama de BD, datos de muestra JSON, restricciones y vistas
App/             # Backend de la aplicación (FastAPI)
```

---

## Requisitos previos

- Python 3.10 o superior
- MongoDB disponible (local o en la nube con MongoDB Atlas)
- pip

---

## Variables de entorno

Antes de ejecutar el proyecto, crea un archivo `.env` dentro de la carpeta `App/` con la URI de conexión a tu base de datos MongoDB:

```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=eventos_db
```

> Si usas MongoDB Atlas, reemplaza `MONGO_URI` con la cadena de conexión de tu cluster.

---

## Instalación y Ejecución

```bash
cd App
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Acceso a la API

- URL base: http://127.0.0.1:8000
- Documentación interactiva (Swagger): http://127.0.0.1:8000/docs
- Documentación alternativa (ReDoc): http://127.0.0.1:8000/redoc

---

## Documentación del proyecto

La carpeta `Documentacion/` contiene los documentos que definen el contexto del proyecto: definición general, modelo de dominio, diagrama de clases y especificación de los servicios REST con responsables asignados.

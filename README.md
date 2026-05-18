# Arquitectura de Servicios - Gestión de Eventos y Actividades

Repositorio del proyecto académico de la materia Arquitectura de Servicios. El sistema tiene como propósito gestionar alumnos, carreras, grupos, eventos, actividades e inscripciones mediante una API REST y una base de datos documental.

## Integrantes

- Fernando Santos Gómez
- Francisco Daniel Arciniega Robles
- Angel Ramón Ramírez Mendoza

## Descripción general

Este proyecto está orientado al desarrollo de una solución para la gestión de eventos y actividades dirigidas a alumnos. A partir del modelo de dominio definido, se documentaron los recursos principales del sistema y las operaciones REST correspondientes para su implementación.

Los recursos contemplados en el sistema son los siguientes:

- Alumno
- Carrera
- Grupo
- Evento
- Actividad
- Inscripción

## Objetivo del repositorio

Este repositorio concentra los componentes principales del proyecto, organizados en carpetas para separar la documentación, la base de datos y el desarrollo de la aplicación. Su propósito es facilitar el trabajo colaborativo del equipo y mantener trazabilidad de avances mediante commits.

## Tecnologías de desarrollo

- Python
- FastAPI
- MongoDB
- API REST

## Contenido de las carpetas

### Documentacion

Contiene los documentos que definen el contexto del proyecto, entre ellos la definición general, el modelo de dominio, el diagrama de clases y el documento de definición de los servicios REST.

### BD

Contiene los elementos relacionados con la base de datos documental del proyecto, incluyendo:

- Diagrama de la base de datos
- Archivos JSON con datos de muestra
- Restricciones de integridad y validaciones de esquemas
- Vistas para simplificar consultas

### App

Contiene la estructura base y los componentes de desarrollo del backend de la aplicación, organizados en módulos para configuración, conexión a base de datos, modelos, rutas y servicios.

## Responsables por recurso

- Alumno: Francisco Daniel Arciniega Robles
- Carrera: Angel Ramón Ramírez Mendoza
- Grupo: Francisco Daniel Arciniega Robles
- Evento: Fernando Santos Gómez
- Actividad: Angel Ramón Ramírez Mendoza
- Inscripción: Fernando Santos Gómez

## Ejecución del backend

### 1. Ingresar a la carpeta de la aplicación

```bash
cd App
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

### 4. Acceder a la API

- URL base: http://127.0.0.1:8000
- Documentación interactiva: http://127.0.0.1:8000/docs

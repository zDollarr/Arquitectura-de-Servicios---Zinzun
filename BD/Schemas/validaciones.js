use gestion_eventos_db;

// Validación para alumnos
db.runCommand({
  collMod: "alumnos",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nombre", "email", "password", "numeroControl", "rol", "tipo", "semestre", "idCarrera", "idGrupo"],
      properties: {
        nombre: { bsonType: "string" },
        email: { bsonType: "string" },
        password: { bsonType: "string", minLength: 6 },
        numeroControl: { bsonType: "string" },
        rol: { bsonType: "string" },
        tipo: { bsonType: "string" },
        estatus: { bsonType: "bool" },
        semestre: { bsonType: "int", minimum: 1 },
        idCarrera: { bsonType: "objectId" },
        idGrupo: { bsonType: "objectId" },
        fechaCreacion: { bsonType: "date" }
      }
    }
  }
});

db.alumnos.createIndex({ email: 1 }, { unique: true });
db.alumnos.createIndex({ numeroControl: 1 }, { unique: true });

// Validación para carreras
db.runCommand({
  collMod: "carreras",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nombre"],
      properties: {
        nombre: { bsonType: "string" },
        estatus: { bsonType: "bool" },
        fechaCreacion: { bsonType: "date" }
      }
    }
  }
});

db.carreras.createIndex({ nombre: 1 }, { unique: true });

// Validación para grupos
db.runCommand({
  collMod: "grupos",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nombre", "idCarrera", "semestre"],
      properties: {
        nombre: { bsonType: "string" },
        idCarrera: { bsonType: "objectId" },
        semestre: { bsonType: "int", minimum: 1 },
        estatus: { bsonType: "bool" },
        fechaCreacion: { bsonType: "date" }
      }
    }
  }
});

// Validación para eventos
db.runCommand({
  collMod: "eventos",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nombre", "fechaInicio", "capacidadMaxima", "descripcion", "tipo"],
      properties: {
        nombre: { bsonType: "string" },
        fechaInicio: { bsonType: "date" },
        capacidadMaxima: { bsonType: "int", minimum: 1 },
        inscritos: { bsonType: "int", minimum: 0 },
        estatus: { bsonType: "string" },
        descripcion: { bsonType: "string" },
        tipo: { bsonType: "string" },
        fechaRegistro: { bsonType: "date" }
      }
    }
  }
});

// Validación para actividades
db.runCommand({
  collMod: "actividades",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nombre", "descripcion", "idEvento", "fecha"],
      properties: {
        nombre: { bsonType: "string" },
        descripcion: { bsonType: "string" },
        idEvento: { bsonType: "objectId" },
        fecha: { bsonType: "date" },
        estatus: { bsonType: "bool" }
      }
    }
  }
});

// Validación para inscripciones
db.runCommand({
  collMod: "inscripciones",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["idAlumno", "idEvento", "fechaInscripcion", "asistencia"],
      properties: {
        idAlumno: { bsonType: "objectId" },
        idEvento: { bsonType: "objectId" },
        fechaInscripcion: { bsonType: "date" },
        asistencia: { bsonType: "bool" }
      }
    }
  }
});

db.inscripciones.createIndex({ idAlumno: 1, idEvento: 1 }, { unique: true });

print("Validaciones aplicadas correctamente");
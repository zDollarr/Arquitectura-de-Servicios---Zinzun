db = db.getSiblingDB("gestion_eventos_db");

// Vista: alumnos con datos de carrera y grupo
db.createView("vista_alumnos_completo", "alumnos", [
  {
    $lookup: {
      from: "carreras",
      localField: "idCarrera",
      foreignField: "_id",
      as: "carrera"
    }
  },
  {
    $lookup: {
      from: "grupos",
      localField: "idGrupo",
      foreignField: "_id",
      as: "grupo"
    }
  },
  {
    $unwind: { path: "$carrera", preserveNullAndEmptyArrays: true }
  },
  {
    $unwind: { path: "$grupo", preserveNullAndEmptyArrays: true }
  },
  {
    $project: {
      password: 0
    }
  }
]);

// Vista: inscripciones con datos del alumno y evento
db.createView("vista_inscripciones_detalle", "inscripciones", [
  {
    $lookup: {
      from: "alumnos",
      localField: "idAlumno",
      foreignField: "_id",
      as: "alumno"
    }
  },
  {
    $lookup: {
      from: "eventos",
      localField: "idEvento",
      foreignField: "_id",
      as: "evento"
    }
  },
  {
    $unwind: { path: "$alumno", preserveNullAndEmptyArrays: true }
  },
  {
    $unwind: { path: "$evento", preserveNullAndEmptyArrays: true }
  },
  {
    $project: {
      "alumno.password": 0
    }
  }
]);

// Vista: eventos con conteo de actividades
db.createView("vista_eventos_con_actividades", "eventos", [
  {
    $lookup: {
      from: "actividades",
      localField: "_id",
      foreignField: "idEvento",
      as: "actividades"
    }
  },
  {
    $addFields: {
      totalActividades: { $size: "$actividades" }
    }
  },
  {
    $project: {
      actividades: 0
    }
  }
]);

db.createView("vista_carreras_con_grupos", "carreras", [
  {
    $lookup: {
      from: "grupos",
      localField: "_id",
      foreignField: "idCarrera",
      as: "grupos"
    }
  },
  {
    $addFields: {
      totalGrupos: { $size: "$grupos" }
    }
  },
  {
    $project: {
      nombre: 1,
      estatus: 1,
      fechaCreacion: 1,
      totalGrupos: 1,
      grupos: {
        _id: 1,
        nombre: 1,
        semestre: 1,
        estatus: 1
      }
    }
  }
]);

print("Vistas creadas correctamente");
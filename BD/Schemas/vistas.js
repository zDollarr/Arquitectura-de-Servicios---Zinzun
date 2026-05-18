use gestion_eventos_db;

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

print("Vistas creadas correctamente");
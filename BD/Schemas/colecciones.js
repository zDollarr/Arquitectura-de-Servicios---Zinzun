db = db.getSiblingDB("gestion_eventos_db");

const colecciones = [
  "alumnos",
  "carreras",
  "grupos",
  "eventos",
  "actividades",
  "inscripciones"
];

colecciones.forEach((nombre) => {
  if (!db.getCollectionNames().includes(nombre)) {
    db.createCollection(nombre);
    print("Colección creada: " + nombre);
  } else {
    print("La colección ya existe: " + nombre);
  }
});

print("Colecciones revisadas correctamente");
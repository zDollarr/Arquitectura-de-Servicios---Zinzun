use gestion_eventos_db;

db.createCollection("alumnos");
db.createCollection("carreras");
db.createCollection("grupos");
db.createCollection("eventos");
db.createCollection("actividades");
db.createCollection("inscripciones");

print("Colecciones creadas correctamente");
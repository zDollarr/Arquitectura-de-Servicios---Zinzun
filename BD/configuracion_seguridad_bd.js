use gestion_eventos_db;

db.createRole({
  role: "administrador_eventos",
  privileges: [
    {
      resource: { db: "gestion_eventos_db", collection: "" },
      actions: ["find", "insert", "update", "remove"]
    }
  ],
  roles: []
});

db.createRole({
  role: "organizador_eventos",
  privileges: [
    {
      resource: { db: "gestion_eventos_db", collection: "eventos" },
      actions: ["find", "insert", "update"]
    },
    {
      resource: { db: "gestion_eventos_db", collection: "actividades" },
      actions: ["find", "insert", "update", "remove"]
    }
  ],
  roles: []
});

db.createRole({
  role: "alumno_eventos",
  privileges: [
    {
      resource: { db: "gestion_eventos_db", collection: "inscripciones" },
      actions: ["find", "insert", "remove"]
    }
  ],
  roles: []
});
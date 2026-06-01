use gestion_eventos_db;

db.alumnos.insertMany([
  {
    nombre: "Admin Usuario",
    email: "admin@itesz.edu.mx",
    password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIr9olWe7e",
    numeroControl: "ADMIN001",
    rol: "admin",
    tipo: "administrador",
    semestre: 0,
    estatus: true,
    fechaCreacion: new Date()
  },
  {
    nombre: "Organizador Usuario",
    email: "organizador@itesz.edu.mx",
    password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIr9olWe7e",
    numeroControl: "ORG001",
    rol: "organizador",
    tipo: "organizador",
    semestre: 0,
    estatus: true,
    fechaCreacion: new Date()
  },
  {
    nombre: "Alumno Prueba",
    email: "alumno@itesz.edu.mx",
    password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIr9olWe7e",
    numeroControl: "20240001",
    rol: "alumno",
    tipo: "regular",
    semestre: 8,
    estatus: true,
    fechaCreacion: new Date()
  }
]);

print("Usuarios creados. Password para todos: password123");
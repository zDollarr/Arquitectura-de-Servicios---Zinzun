from fastapi import FastAPI

app = FastAPI(
    title="API Gestión de Eventos y Actividades",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
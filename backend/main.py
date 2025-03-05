from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import router

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(router)

@app.get("/")
def read_root():
    return {"mensaje": "API de gestión de trabajadores funcionando correctamente"}

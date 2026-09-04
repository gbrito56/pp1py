from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.articulos import router as articulos_router
from src.database import engine, Base

Base.metadata.create_all(bind=engine)  # Crea las tablas en la DB si no existen

app = FastAPI()

app.title = "API Libreria - Gestión de Inventario"  # Cambia el nombre en /docs

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500", #Habilita para desarrollo local (?)
        # "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articulos_router)

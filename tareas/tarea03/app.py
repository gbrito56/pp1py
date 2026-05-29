from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()

app.title = "API Libreria"  # Cambia el nombre en /docs

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        # "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Artículo no encontrado",
                }
            }
        },
    },
}

IntPositivo = Annotated[int, Field(gt=0)]
StrCortito = Annotated[str, Field(max_length=30)]
IntPrecioVenta = Annotated[int, Field(ge=500, lt=999999)]
BoolActivo = Annotated[bool, Field(description="Sigue disponible?")]
IdBuscado = Annotated[int, Path(gt=0)]

class ArticuloSchema(BaseModel):
    id: Annotated[int, Field(gt=0, description="ID del articulo", deprecated=True)]
    nombre: StrCortito
    precio: IntPrecioVenta = 1500
    activo: BoolActivo = True

class ArticuloNuevoSchema(BaseModel):
    nombre: StrCortito
    precio: IntPrecioVenta
    activo: BoolActivo = True

class ArticuloUpdateSchema(BaseModel):
    nombre: StrCortito
    precio: IntPrecioVenta = 2000
    activo: BoolActivo = True

articulos = [
    {"id": 1, "nombre": "Cuaderno A4", "precio": 2500, "activo": True},
    {"id": 2, "nombre": "Bolígrafo Azul", "precio": 1500, "activo": True},
    {"id": 3, "nombre": "Marcador Resaltador", "precio": 1800, "activo": True},
    {"id": 4, "nombre": "Goma de Borrar", "precio": 600, "activo": True},
    {"id": 5, "nombre": "Tijeras de Mano", "precio": 3500, "activo": True},
    {"id": 6, "nombre": "Regla de 30cm", "precio": 1200, "activo": True},
    {"id": 7, "nombre": "Lápiz de Grafito", "precio": 800, "activo": True},
    {"id": 8, "nombre": "Estuche para lápices", "precio": 3500, "activo": True},
    {"id": 9, "nombre": "Calculadora Científica", "precio": 15000, "activo": True},
    {"id": 10, "nombre": "Archivador", "precio": 4500, "activo": True},
]

@app.get("/articulos", response_model=list[ArticuloSchema])
async def get_articulos():
    return articulos

@app.get("/articulos/{id}", responses=NOT_FOUND_RESPONSE, response_model=ArticuloSchema)
async def get_articulos_by_id(
    id: IdBuscado,
):
    for articulo in articulos:
        if articulo["id"] == id:
            return articulo
    raise HTTPException(status_code=404, detail="Artículo no encontrado")

@app.post("/articulos", response_model=list[ArticuloSchema])
async def crear_articulo(articulo_nuevo: ArticuloNuevoSchema):
    max_id = max(a["id"] for a in articulos) if articulos else 0
    nuevo_id = max_id + 1
    nuevo_articulo = {
        "id": nuevo_id,
        "nombre": articulo_nuevo.nombre,
        "precio": articulo_nuevo.precio,
        "activo": articulo_nuevo.activo,
    }
    articulos.append(nuevo_articulo)
    return articulos

@app.delete("/articulos/{id}", responses=NOT_FOUND_RESPONSE, response_model=ArticuloSchema)
async def borrar_articulo(
    id: IdBuscado,
    logico: Annotated[bool, Query(description="Mantener registro?")] = False,
) -> ArticuloSchema:
    for articulo in articulos:
        if articulo["id"] == id:
            if logico:
                articulo["activo"] = False
            else:
                articulos.remove(articulo)
            return articulo
    raise HTTPException(status_code=404, detail="Artículo no encontrado")

@app.put("/articulos/{id}", responses=NOT_FOUND_RESPONSE, response_model=ArticuloSchema)
async def editar_articulo(
    id: Annotated[int, Path(gt=0, description="Id del producto.")],
    articulo_editar: ArticuloUpdateSchema,
):
    for articulo in articulos:
        if articulo["id"] == id:
            articulo["nombre"] = articulo_editar.nombre
            articulo["precio"] = articulo_editar.precio
            articulo["activo"] = articulo_editar.activo
            return articulo
    raise HTTPException(status_code=404, detail="Articulo no encontrado")

"""

# Parámetro query-> /articulos?clave=valor&llave=valor
# validacion para int
# gt greater than : mayor que
# ge greater or equal : >= que
# lt less than : menor que
# le less or equal : <= que
# max_digits / min_digits
# para str
# min_length
# max_length

"""

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()

app.title = "Mi primera API"  # Cambia el nombre en /docs

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",  # entorno desarrollo
        "https://faculemo.github.io/front",  # entorno producción
        # "*", -Cualquier origen-
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NOT_FOUND_RESPONSE = { # Constante, mayúsculas con snake_case
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
IntPrecioVenta = Annotated[int, Field(gt=500, lt=999999)]
BoolActivo = Annotated[bool, Field(description="Sigue disponible?")]

class ArticuloSchema(BaseModel):
    id: Annotated[int, Field(gt=0, description="ID del articulo", deprecated=True)]
    nombre: StrCortito
    precio: IntPrecioVenta = 1500
    activo: BoolActivo = True

class ArticuloUpdateSchema(BaseModel):
    nombre: StrCortito
    precio: IntPrecioVenta = 2000
    activo: BoolActivo = True

articulos = [
    {"id": 1, "nombre": "Cuaderno A4", "precio": 2500, "activo": True},
    {"id": 2, "nombre": "Bolígrafo Azul", "precio": 1500, "activo": True},
    {"id": 3, "nombre": "Marcador Resaltador", "precio": 1800, "activo": True},
    {"id": 4, "nombre": "Goma de Borrar", "precio": 500, "activo": True},
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

@app.get(
    "/articulos/{id}",  # Parámetro de ruta (esta en la url)
    responses=NOT_FOUND_RESPONSE,
    response_model=ArticuloSchema,
)
async def get_articulos_by_id(
    id: Annotated[int, Path(gt=0)],
    # ^^El tipo de este parámetro podría ser modularizado, ¿no?
):
    for articulo in articulos:
        if articulo["id"] == id:
            return articulo
    raise HTTPException(status_code=404, detail="Artículo no encontrado")

@app.post("/articulos", response_model=list[ArticuloSchema])
async def crear_articulo(articulo_nuevo: ArticuloSchema):
    articulos.append(articulo_nuevo.model_dump())
    return articulos

@app.delete(
    "/articulos/{id}",  # ?logico=false
    responses=NOT_FOUND_RESPONSE,
    response_model=ArticuloSchema,
)
async def borrar_articulo(
    id: Annotated[int, Path(gt=0)],
    logico: Annotated[bool, Query(description="Mantener registro?")] = False,
    # ^^ los tipos de estos parámetros pueden ser modularizados, ¿no?
) -> ArticuloSchema:
    for articulo in articulos:
        if articulo["id"] == id:
            if logico:
                articulo["activo"] = (False,)
            else:
                articulos.remove(articulo)
            return articulo
    raise HTTPException(status_code=404, detail="Artículo no encontrado")

@app.put("/articulos/{id}", responses=NOT_FOUND_RESPONSE, response_model=ArticuloSchema)
async def editar_articulo(
    id: Annotated[int, Path(gt=0, description="Id del producto. >0")],
    # ^^ El tipo puede ser modularizado, no?
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

@app.get("/saludar")
async def saludar():
    return {"Hola": "Mundo"}
@app.post("/saludar/post")
async def post():
    return {"Hola": "Post"}
@app.put("/saludar/put")
async def put():
    return {"Hola": "Put"}
@app.delete("/saludar/delete")
async def delete():
    return {"Hola": "Delete"}
"""

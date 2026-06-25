from fastapi import APIRouter, HTTPException, Path, Query
from typing import Annotated
import src.schemas.articulos as schemas

router = APIRouter(prefix="/articulos", tags=["Operaciones con artículos"])

articulos = [
    {"id": 1, "nombre": "Cuaderno A4", "precio": 2500, "activo": True},
    {"id": 2, "nombre": "Lapicera Azul", "precio": 1500, "activo": True},
    {"id": 3, "nombre": "Resaltador", "precio": 1800, "activo": True},
    {"id": 4, "nombre": "Goma de Borrar", "precio": 600, "activo": True},
    {"id": 5, "nombre": "Tijera 12cm", "precio": 3500, "activo": True},
    {"id": 6, "nombre": "Regla de 30cm", "precio": 1200, "activo": True},
    {"id": 7, "nombre": "Lápiz Negro", "precio": 800, "activo": True},
    {"id": 8, "nombre": "Cartuchera", "precio": 3500, "activo": True},
    {"id": 9, "nombre": "Calculadora Científica", "precio": 15000, "activo": True},
    {"id": 10, "nombre": "Bibliorato", "precio": 4500, "activo": True},
]

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

@router.get("", response_model=list[schemas.ArticuloSchema])
async def mostrar_articulos():
    return articulos

@router.get("/{id}", responses=NOT_FOUND_RESPONSE, response_model=schemas.ArticuloSchema)
async def mostrar_articulos_por_id(
    id: schemas.IdBuscado,
):
    for articulo in articulos:
        if articulo["id"] == id:
            return articulo
    raise HTTPException(status_code=404, detail="Artículo no encontrado")

@router.post("", response_model=list[schemas.ArticuloSchema])
async def crear_articulo(articulo_nuevo: schemas.ArticuloNuevoSchema):
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

@router.delete("/{id}", responses=NOT_FOUND_RESPONSE, response_model=schemas.ArticuloSchema)
async def borrar_articulo(
    id: schemas.IdBuscado,
    logico: Annotated[bool, Query(description="Mantener registro?")] = False,
) -> schemas.ArticuloSchema:
    for articulo in articulos:
        if articulo["id"] == id:
            if logico:
                articulo["activo"] = False
            else:
                articulos.remove(articulo)
            return articulo
    raise HTTPException(status_code=404, detail="Artículo no encontrado")

@router.put("/{id}", responses=NOT_FOUND_RESPONSE, response_model=schemas.ArticuloSchema)
async def editar_articulo(
    id: Annotated[int, Path(gt=0, description="Id del producto.")],
    articulo_editar: schemas.ArticuloUpdateSchema,
):
    for articulo in articulos:
        if articulo["id"] == id:
            articulo["nombre"] = articulo_editar.nombre
            articulo["precio"] = articulo_editar.precio
            articulo["activo"] = articulo_editar.activo
            return articulo
    raise HTTPException(status_code=404, detail="Articulo no encontrado")

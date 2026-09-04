from fastapi import APIRouter, HTTPException, Path, Query, Depends
from typing import Annotated
import src.schemas.articulos as schemas
from src.models.articulos import Articulo
from sqlalchemy.orm import Session
from src.database import get_db

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

#Obtener todos los articulos

@router.get("", response_model=list[schemas.ArticuloSchema])
async def mostrar_articulos(db: Session = Depends(get_db)):
    articulos = db.query(Articulo).all()
    return articulos

#Obtener articulo por id

@router.get("/{id}", responses=NOT_FOUND_RESPONSE, response_model=schemas.ArticuloSchema)

async def mostrar_articulos_por_id(
    id: schemas.IdBuscado,
    db: Session = Depends(get_db)
):
    #articulo_obtenido
    articulo_obtenido = db.get(Articulo, id)
    if articulo_obtenido is not None:
        return articulo_obtenido
    raise HTTPException(status_code=404, detail="Artículo no encontrado")

#Modificar articulo

@router.post("", response_model=list[schemas.ArticuloSchema])

async def crear_articulo(articulo_nuevo: schemas.ArticuloNuevoSchema, db: Session = Depends(get_db)):
    articulo_db = Articulo(
        nombre=articulo_nuevo.nombre,
        precio=articulo_nuevo.precio,
        activo=articulo_nuevo.activo
    )
    db.add(articulo_db)
    db.commit()
    db.refresh(articulo_db)
    return articulo_db

#Modificar articulo

@router.put("/{id}", responses=NOT_FOUND_RESPONSE, response_model=schemas.ArticuloSchema)
async def editar_articulo(
    id: Annotated[int, Path(gt=0, description="Id del producto.")],
    articulo_editar: schemas.ArticuloUpdateSchema, db: Session = Depends(get_db)
):
    articulo_obtenido = db.get(Articulo, id)
    if articulo_obtenido is not None:
        articulo_obtenido.nombre = articulo_editar.nombre
        articulo_obtenido.precio = articulo_editar.precio
        articulo_obtenido.activo = articulo_editar.activo
        db.commit()
        db.refresh(articulo_obtenido)
        return articulo_obtenido
    raise HTTPException(status_code=404, detail="Articulo no encontrado")

#Borrar articulo

@router.delete("/{id}", responses=NOT_FOUND_RESPONSE, response_model=list[schemas.ArticuloSchema])

async def borrar_articulo(
    id: schemas.IdBuscado,
    db: Session = Depends(get_db),
    logico: Annotated[bool, Query(description="Mantener registro?")] = False
) -> list[schemas.ArticuloSchema]:
    articulo_obtenido = db.get(Articulo, id)
    if articulo_obtenido is not None:
        if logico:
            articulo_obtenido.activo = False
        else:
            db.delete(articulo_obtenido)
        db.commit()
        return db.query(Articulo).all()
    raise HTTPException(status_code=404, detail="Artículo no encontrado")
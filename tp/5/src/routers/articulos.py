from fastapi import APIRouter, HTTPException, Path, Query, Depends
from typing import Annotated
from src.models.articulos import (
    Articulo,
    ArticuloCreate,
    ArticuloPublic,
    ArticuloPublicNested,
    Marca,
    MarcaCreate,
    MarcaPublic,
    MarcaPublicNested,
    Proveedor,
    ProveedorCreate,
    ProveedorPublic,
    ProveedorPublicNested,
)
from src.database import get_db
from sqlmodel import Session, select

router = APIRouter(prefix="/articulos")

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Elemento no encontrado",
                }
            }
        },
    },
}

# Marcas

# Crear

@router.post("/marcas", tags=["Marcas"], response_model=MarcaPublic)

async def crear_marca(marca_nueva: MarcaCreate, db: Session = Depends(get_db)):
    marca_db = Marca.model_validate(marca_nueva)
    db.add(marca_db)
    db.commit()
    db.refresh(marca_db)
    return marca_db

# Mostrar marca

@router.get("/marcas/{id}", tags=["Marcas"], responses=NOT_FOUND_RESPONSE, response_model=MarcaPublicNested)

async def mostrar_marca(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db)
):
    marca = db.get(Marca, id)
    if marca is not None:
        return marca
    raise HTTPException(status_code=404, detail="Marca no encontrada")

# Proveedores

# Crear

@router.post("/proveedores", tags=["Proveedores"], response_model=ProveedorPublic)

async def crear_proveedor(proveedor_nuevo: ProveedorCreate, db: Session = Depends(get_db)):
    proveedor_db = Proveedor.model_validate(proveedor_nuevo)
    db.add(proveedor_db)
    db.commit()
    db.refresh(proveedor_db)
    return proveedor_db

# Mostrar proveedor

@router.get("/proveedores/{id}", tags=["Proveedores"], responses=NOT_FOUND_RESPONSE, response_model=ProveedorPublicNested)

async def mostrar_proveedor(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db)
):
    proveedor = db.get(Proveedor, id)
    if proveedor is not None:
        return proveedor
    raise HTTPException(status_code=404, detail="Proveedor no encontrado")

# Articulos

# Listar articulos

@router.get("", tags=["Artículos"], response_model=list[ArticuloPublic])
async def mostrar_articulos(db: Session = Depends(get_db)):
    articulos = db.exec(select(Articulo)).all()
    return articulos

# Buscar por id

@router.get("/{id}", tags=["Artículos"], responses=NOT_FOUND_RESPONSE, response_model=ArticuloPublicNested)

async def mostrar_articulos_por_id(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db)
):
    art_obtenido = db.get(Articulo, id)
    if art_obtenido is not None:
        return art_obtenido
    raise HTTPException(status_code=404, detail="Artículo no encontrado")

# Crear

@router.post("", tags=["Artículos"], response_model=ArticuloPublic)

async def crear_articulo(articulo_nuevo: ArticuloCreate, db: Session = Depends(get_db)):
    art_db = Articulo.model_validate(articulo_nuevo)
    db.add(art_db)
    db.commit()
    db.refresh(art_db)
    return art_db

# Modificar

@router.put("/{id}", tags=["Artículos"], responses=NOT_FOUND_RESPONSE, response_model=ArticuloPublic)
async def editar_articulo(
    id: Annotated[int, Path(gt=0, description="Id del producto.")],
    articulo_editar: ArticuloCreate, db: Session = Depends(get_db)
):
    art_obtenido = db.get(Articulo, id)
    if art_obtenido is not None:
        art_obtenido.nombre = articulo_editar.nombre
        art_obtenido.precio = articulo_editar.precio
        art_obtenido.activo = articulo_editar.activo
        art_obtenido.marca_id = articulo_editar.marca_id
        art_obtenido.proveedor_id = articulo_editar.proveedor_id
        db.commit()
        db.refresh(art_obtenido)
        return art_obtenido
    raise HTTPException(status_code=404, detail="Articulo no encontrado")

# Borrar

@router.delete("/{id}", tags=["Artículos"], responses=NOT_FOUND_RESPONSE, response_model=list[ArticuloPublic])

async def borrar_articulo(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db),
    logico: Annotated[bool, Query(description="Mantener registro?")] = False
) -> list[ArticuloPublic]:
    art_obtenido = db.get(Articulo, id)
    if art_obtenido is not None:
        if logico:
            art_obtenido.activo = False
        else:
            db.delete(art_obtenido)
        db.commit()
        return db.exec(select(Articulo)).all()
    raise HTTPException(status_code=404, detail="Artículo no encontrado")

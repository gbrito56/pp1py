from fastapi import Path
from typing import Annotated
from pydantic import BaseModel, Field

IntPositivo = Annotated[int, Field(gt=0)]
StrCortito = Annotated[str, Field(max_length=30)]
IntPrecioVenta = Annotated[int, Field(ge=500, lt=999999)]
BoolActivo = Annotated[bool, Field(description="Sigue disponible?")]
IdBuscado = Annotated[int, Path(gt=0)]

class ArticuloSchema(BaseModel): #modelo de articulo
    id: Annotated[int, Field(gt=0, description="ID del articulo", deprecated=True)]
    nombre: StrCortito
    precio: IntPrecioVenta = 1500
    activo: BoolActivo = True

class ArticuloNuevoSchema(BaseModel): #modelo de articulo nuevo
    nombre: StrCortito
    precio: IntPrecioVenta
    activo: BoolActivo = True

class ArticuloUpdateSchema(BaseModel): #modelo de edicion de articulo
    nombre: StrCortito
    precio: IntPrecioVenta = 2000
    activo: BoolActivo = True

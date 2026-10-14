#Clases que representan tablas en la DB

from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

# Marca

class MarcaBase(SQLModel):
    nombre: str = Field(index=True)

class Marca(MarcaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    articulos: List["Articulo"] = Relationship(back_populates="marca")

class MarcaCreate(MarcaBase):
    pass

class MarcaPublic(MarcaBase):
    id: int

# Proveedor

class ProveedorBase(SQLModel):
    nombre: str = Field(index=True)
    direccion: Optional[str] = None
    telefono: Optional[int] = None

class Proveedor(ProveedorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    articulos: List["Articulo"] = Relationship(back_populates="proveedor")

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorPublic(ProveedorBase):
    id: int

# Articulo

class ArticuloBase(SQLModel):
    nombre: str = Field(index=True)
    precio: int
    activo: bool
    marca_id: Optional[int] = Field(default=None, foreign_key="marca.id")
    proveedor_id: Optional[int] = Field(default=None, foreign_key="proveedor.id")


class Articulo(ArticuloBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    marca: Optional[Marca] = Relationship(back_populates="articulos")
    proveedor: Optional[Proveedor] = Relationship(back_populates="articulos")

class ArticuloCreate(ArticuloBase):
    pass

class ArticuloPublic(ArticuloBase):
    id: int

# Nested

class ArticuloPublicNested(ArticuloPublic):
    marca: Optional[MarcaPublic] = None
    proveedor: Optional[ProveedorPublic] = None

class ProveedorPublicNested(ProveedorPublic):
    articulos: Optional[List[ArticuloPublic]] = []

class MarcaPublicNested(MarcaPublic):
    articulos: Optional[List[ArticuloPublic]] = []

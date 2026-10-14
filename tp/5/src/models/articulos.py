#Clases que representan tablas en la DB

from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

# Marca

class MarcaBase(SQLModel):
    nombre: str = Field(index=True)
    origen_id: Optional[int] = Field(default=None, foreign_key="origen.id")

class Marca(MarcaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    origen: Optional["Origen"] = Relationship(back_populates="marcas")
    articulos: List["Articulo"] = Relationship(back_populates="marca")

class MarcaCreate(MarcaBase):
    pass

class MarcaPublic(MarcaBase):
    id: int

# Origen

class OrigenBase(SQLModel):
    pais: str = Field(index=True)

class Origen(OrigenBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    marcas: List[Marca] = Relationship(back_populates="origen")

class OrigenCreate(OrigenBase):
    pass

class OrigenPublic(OrigenBase):
    id: int

# Articulo

class ArticuloBase(SQLModel):
    nombre: str = Field(index=True)
    precio: int
    activo: bool
    marca_id: Optional[int] = Field(default=None, foreign_key="marca.id")


class Articulo(ArticuloBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    marca: Optional[Marca] = Relationship(back_populates="articulos")

class ArticuloCreate(ArticuloBase):
    pass

class ArticuloPublic(ArticuloBase):
    id: int

# Nested

class ArticuloPublicNested(ArticuloPublic):
    marca: Optional[MarcaPublic] = None

class OrigenPublicNested(OrigenPublic):
    marcas: Optional[List[MarcaPublic]] = []

class MarcaPublicNested(MarcaPublic):
    articulos: Optional[List[ArticuloPublic]] = []

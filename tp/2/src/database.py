#Conexion hacia la DB real mediante SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

url = "sqlite:///./database.db"

#FastAPI es asincrono, por lo que se debe indicar que no se debe chequear el hilo de ejecución: 2do argumento

engine = create_engine(url, connect_args={"check_same_thread": False})

#Nos permite la conexion a traves del motor

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Clase que representa la tabla

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db #Return sin finalizar la funcion
    finally:
        db.close()
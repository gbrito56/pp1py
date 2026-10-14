#Conexion hacia la DB real mediante SQLModel

from sqlmodel import create_engine, Session, SQLModel

url = "sqlite:///./database_sqlmodel.db" # URL de la base de datos

#Nos permite la conexion a traves del motor
#FastAPI es asincrono, por lo que se debe indicar que no se debe chequear el hilo de ejecución: 2do argumento

engine = create_engine(url, connect_args={"check_same_thread": False})

def get_db():
    with Session(engine) as db:
        yield db
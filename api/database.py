# Este archivo es el "puente" con MySQL. Abre la conexión y nos da una sesión
# para que en cada endpoint podamos hablar con la base de datos sin enredarnos.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Si tu XAMPP usa root sin clave, esto funciona tal cual.
# Si tienes clave, agrega :password  ->  mysql+pymysql://root:TU_CLAVE@localhost/proyecto_tech
DATABASE_URL = "mysql+pymysql://root:@localhost/proyecto"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Esta función me entrega una sesión de BD lista para usar y luego la cierra.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

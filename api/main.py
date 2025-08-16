# Este archivo es el que enciende todo. Piensa que es el "switch" de la API.
# Aqui levanto FastAPI, conecto cada grupo de rutas (endpoints) y
# habilito CORS y los archivos estaticos para servir las imagenes subidas.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Importo los routers (las rutas de cada modulo)
from routes import users, clients, providers, products, services, purchases

app = FastAPI(title="Proyecto Tech API", version="1.0")

# CORS para permitir que el frontend (tu HTML/JS) le pegue a esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # En produccion conviene restringir a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enlazo cada grupo de rutas con su prefijo
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(clients.router, prefix="/api/clients", tags=["Clients"])
app.include_router(providers.router, prefix="/api/providers", tags=["Providers"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(services.router, prefix="/api/services", tags=["Services"])
app.include_router(purchases.router, prefix="/api/purchases", tags=["Purchases"])

# Aqui sirvo las imagenes que se suban (p.ej. /uploads/products/xxx.png)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def root():
    # Mini saludo para comprobar que esta arriba
    return {"message": "API Proyecto Tech funcionando :)"}

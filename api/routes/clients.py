# CRUD de clientes. Nada raro: crear, listar, ver, actualizar y eliminar.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Client
from schemas import ClientCreate, ClientOut

router = APIRouter()

@router.get("/", response_model=List[ClientOut])
def list_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@router.get("/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db)):
    c = db.query(Client).get(client_id)
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return c

@router.post("/", response_model=ClientOut)
def create_client(client_in: ClientCreate, db: Session = Depends(get_db)):
    c = Client(**client_in.dict())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.put("/{client_id}", response_model=ClientOut)
def update_client(client_id: int, client_in: ClientCreate, db: Session = Depends(get_db)):
    c = db.query(Client).get(client_id)
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for k, v in client_in.dict().items():
        setattr(c, k, v)
    db.commit()
    db.refresh(c)
    return c

@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    c = db.query(Client).get(client_id)
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(c)
    db.commit()
    return {"message": "Cliente eliminado"}

# CRUD de servicios técnicos. Le dejo técnico asignado opcional (id de users).

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Service
from schemas import ServiceCreate, ServiceOut

router = APIRouter()

@router.get("/", response_model=List[ServiceOut])
def list_services(db: Session = Depends(get_db)):
    return db.query(Service).all()

@router.get("/{service_id}", response_model=ServiceOut)
def get_service(service_id: int, db: Session = Depends(get_db)):
    s = db.query(Service).get(service_id)
    if not s:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return s

@router.post("/", response_model=ServiceOut)
def create_service(service_in: ServiceCreate, db: Session = Depends(get_db)):
    s = Service(**service_in.dict())
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@router.put("/{service_id}", response_model=ServiceOut)
def update_service(service_id: int, service_in: ServiceCreate, db: Session = Depends(get_db)):
    s = db.query(Service).get(service_id)
    if not s:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    for k, v in service_in.dict().items():
        setattr(s, k, v)
    db.commit()
    db.refresh(s)
    return s

@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    s = db.query(Service).get(service_id)
    if not s:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    db.delete(s)
    db.commit()
    return {"message": "Servicio eliminado"}

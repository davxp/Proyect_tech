# CRUD de proveedores. Mismo patrón que clientes.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Provider
from schemas import ProviderCreate, ProviderOut

router = APIRouter()

@router.get("/", response_model=List[ProviderOut])
def list_providers(db: Session = Depends(get_db)):
    return db.query(Provider).all()

@router.get("/{provider_id}", response_model=ProviderOut)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    p = db.query(Provider).get(provider_id)
    if not p:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return p

@router.post("/", response_model=ProviderOut)
def create_provider(provider_in: ProviderCreate, db: Session = Depends(get_db)):
    p = Provider(**provider_in.dict())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.put("/{provider_id}", response_model=ProviderOut)
def update_provider(provider_id: int, provider_in: ProviderCreate, db: Session = Depends(get_db)):
    p = db.query(Provider).get(provider_id)
    if not p:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    for k, v in provider_in.dict().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{provider_id}")
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    p = db.query(Provider).get(provider_id)
    if not p:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    db.delete(p)
    db.commit()
    return {"message": "Proveedor eliminado"}

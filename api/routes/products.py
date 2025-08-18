# CRUD de productos + endpoint para subir imagen y guardar la ruta en image_path.
# Las imágenes se guardan en api/uploads/products y se sirven en /uploads/products/...

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os, shutil

from database import get_db
from models import Product
from schemas import ProductCreate, ProductOut

router = APIRouter()

UPLOAD_DIR = os.path.join("uploads", "products")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = db.query(Product).get(product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p

@router.post("/", response_model=ProductOut)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    p = Product(**product_in.dict())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_in: ProductCreate, db: Session = Depends(get_db)):
    p = db.query(Product).get(product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for k, v in product_in.dict().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    p = db.query(Product).get(product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(p)
    db.commit()
    return {"message": "Producto eliminado"}

@router.post("/{product_id}/upload-image")
def upload_product_image(product_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    p = db.query(Product).get(product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    filename = file.filename
    save_path = os.path.join(UPLOAD_DIR, filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    p.image_path = f"/uploads/products/{filename}"
    db.commit()
    db.refresh(p)
    return {"message": "Imagen subida", "path": p.image_path}

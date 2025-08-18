# Compras con su detalle. Aquí hago el "maestro-detalle":
# creo la compra, inserto sus items y actualizo el total.
# Nota: si quieres también descontar/afectar stock, podrías restarlo aquí.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Purchase, PurchaseItem, Product
from schemas import PurchaseCreate, PurchaseOut, PurchaseItemOut

router = APIRouter()

@router.get("/", response_model=List[PurchaseOut])
def list_purchases(db: Session = Depends(get_db)):
    purchases = db.query(Purchase).all()
    result = []
    for p in purchases:
        items = [PurchaseItemOut.from_orm(i) for i in p.items]
        result.append(PurchaseOut(id=p.id, client_id=p.client_id, total=float(p.total), items=items))
    return result

@router.get("/{purchase_id}", response_model=PurchaseOut)
def get_purchase(purchase_id: int, db: Session = Depends(get_db)):
    p = db.query(Purchase).get(purchase_id)
    if not p:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    items = [PurchaseItemOut.from_orm(i) for i in p.items]
    return PurchaseOut(id=p.id, client_id=p.client_id, total=float(p.total), items=items)

@router.post("/", response_model=PurchaseOut)
def create_purchase(data: PurchaseCreate, db: Session = Depends(get_db)):
    # Creo la compra sin total y luego le meto los items
    purchase = Purchase(client_id=data.client_id, created_by=data.created_by, total=0)
    db.add(purchase)
    db.flush()  # me da el id de la compra sin hacer commit aun

    total = 0
    for it in data.items:
        # opcional: validar que el producto exista
        prod = db.query(Product).get(it.product_id)
        if not prod:
            raise HTTPException(status_code=400, detail=f"Producto {it.product_id} no existe")

        item = PurchaseItem(
            purchase_id=purchase.id,
            product_id=it.product_id,
            quantity=it.quantity,
            price=it.price
        )
        db.add(item)
        total += it.quantity * it.price

        # si quisieras afectar stock del producto, descomenta:
        # prod.stock = (prod.stock or 0) - it.quantity

    purchase.total = total
    db.commit()
    db.refresh(purchase)

    items = [PurchaseItemOut.from_orm(i) for i in purchase.items]
    return PurchaseOut(id=purchase.id, client_id=purchase.client_id, total=float(purchase.total), items=items)

@router.delete("/{purchase_id}")
def delete_purchase(purchase_id: int, db: Session = Depends(get_db)):
    p = db.query(Purchase).get(purchase_id)
    if not p:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    db.delete(p)   # por el cascade, se van los items también
    db.commit()
    return {"message": "Compra eliminada"}

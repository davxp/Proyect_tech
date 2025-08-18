# Endpoints de usuarios. Aquí puedo registrar, listar, ver, actualizar, borrar
# y además tengo un login simple SIN hash (solo texto plano).

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User
from schemas import UserCreate, UserOut, UserBase

router = APIRouter()

# Registrar usuario (guarda la contraseña en texto plano)
@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == user_in.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Ese correo ya está registrado")
    user = User(
        name=user_in.name,
        email=user_in.email,
        role=user_in.role or "user",
        password_hash=user_in.password,   # ⚡ Guardamos directo sin encriptar
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Login con comparación directa
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or user.password_hash != password:  # ⚡ Comparación simple
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {
        "message": "Login OK",
        "user": {"id": user.id, "name": user.name, "role": user.role}
    }

# Listar usuarios
@router.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Ver un usuario
@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# Actualizar usuario
@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_in: UserBase, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.name = user_in.name
    user.email = user_in.email
    user.role = user_in.role or user.role
    db.commit()
    db.refresh(user)
    return user

# Eliminar usuario
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado"}

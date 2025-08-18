# Estos son los "formatos" de entrada/salida (Pydantic).
# Me ayudan a validar lo que recibo por la API y a devolver respuestas limpias.

from pydantic import BaseModel, EmailStr
from typing import Optional, List

# -------- Users --------
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
     from_attributes = True


# -------- Clients --------
class ClientBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: int
    class Config:
         from_attributes = True


# -------- Providers --------
class ProviderBase(BaseModel):
    company_name: str
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class ProviderCreate(ProviderBase):
    pass

class ProviderOut(ProviderBase):
    id: int
    class Config:
        from_attributes = True

# -------- Products --------
class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    provider_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    image_path: Optional[str] = None
    class Config:
     from_attributes = True


# -------- Services --------
class ServiceBase(BaseModel):
    title: str
    description: Optional[str] = None
    cost: float
    estimated_time_minutes: int
    assigned_technician_id: Optional[int] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceOut(ServiceBase):
    id: int
    class Config:
        from_attributes = True

# -------- Purchases --------
class PurchaseItemIn(BaseModel):
    product_id: int
    quantity: int
    price: float

class PurchaseCreate(BaseModel):
    client_id: Optional[int] = None
    created_by: Optional[int] = None
    items: List[PurchaseItemIn]

class PurchaseItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    class Config:
        from_attributes = True

class PurchaseOut(BaseModel):
    id: int
    client_id: Optional[int] = None
    total: float
    items: List[PurchaseItemOut]
    class Config:
        from_attributes = True

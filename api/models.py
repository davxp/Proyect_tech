# Aquí mapeo las tablas de MySQL a clases Python (ORM con SQLAlchemy).
# La idea: trabajar con objetos y que SQLAlchemy traduzca a SQL por mí.

from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user")
    created_at = Column(DateTime, server_default=func.current_timestamp())

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120))
    email = Column(String(150))
    phone = Column(String(50))
    address = Column(Text)
    created_at = Column(DateTime, server_default=func.current_timestamp())

class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=False)
    contact_name = Column(String(150))
    phone = Column(String(50))
    email = Column(String(150))
    created_at = Column(DateTime, server_default=func.current_timestamp())

    products = relationship("Product", back_populates="provider")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(80), unique=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), default=0)
    stock = Column(Integer, default=0)
    provider_id = Column(Integer, ForeignKey("providers.id"))
    image_path = Column(String(255))
    created_at = Column(DateTime, server_default=func.current_timestamp())

    provider = relationship("Provider", back_populates="products")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    cost = Column(DECIMAL(10, 2), default=0)
    estimated_time_minutes = Column(Integer, default=60)
    assigned_technician_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.current_timestamp())

    technician = relationship("User")

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    date = Column(DateTime, server_default=func.current_timestamp())
    total = Column(DECIMAL(12, 2), default=0)
    created_by = Column(Integer, ForeignKey("users.id"))

    client = relationship("Client")
    created_by_user = relationship("User")
    items = relationship("PurchaseItem", cascade="all, delete-orphan", back_populates="purchase")

class PurchaseItem(Base):
    __tablename__ = "purchase_items"
    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(DECIMAL(10, 2))

    purchase = relationship("Purchase", back_populates="items")
    product = relationship("Product")

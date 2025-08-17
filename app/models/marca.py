# app/models/marca_model.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Marca(Base):
    __tablename__ = "marca"

    id = Column(Integer, primary_key=True, index=True)
    nome_marca = Column(String(255), unique=True, nullable=False)

    # CORREÇÃO: Usar string no relationship
    modelos = relationship("Modelo", back_populates="marca")
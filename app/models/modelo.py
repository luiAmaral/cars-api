# app/models/modelo_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base

class Modelo(Base):
    __tablename__ = "modelo"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    valor_fipe = Column(DECIMAL(10, 2), nullable=False)
    
    marca_id = Column(Integer, ForeignKey("marca.id"))

    marca = relationship("Marca", back_populates="modelos")
    carros = relationship("Carro", back_populates="modelo")
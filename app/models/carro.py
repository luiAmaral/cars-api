from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Carro(Base):
    __tablename__ = "carro"

    id = Column(Integer, primary_key=True, index=True)
    timestamp_cadastro = Column(BigInteger, nullable=False)
    ano = Column(Integer, nullable=False)
    combustivel = Column(String(100), nullable=False)
    num_portas = Column(Integer, nullable=False)
    cor = Column(String(100), nullable=False)

    modelo_id = Column(Integer, ForeignKey("modelo.id"))

    modelo = relationship("Modelo", back_populates="carros")
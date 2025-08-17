from pydantic import BaseModel
from typing import List

class CarroBase(BaseModel):
    ano: int
    combustivel: str
    num_portas: int
    cor: str
    modelo_id: int

class CarroCreate(CarroBase):
    pass

class Carro(CarroBase):
    id: int
    timestamp_cadastro: int

    class Config:
        orm_mode = True
        
class CarroUpdate(CarroBase):
    pass

# Schemas para o endpoint customizado
class CarroListing(BaseModel):
    id: int
    timestamp_cadastro: int
    modelo_id: int
    ano: int
    combustivel: str
    num_portas: int
    cor: str
    nome_modelo: str
    valor: float

    class Config:
        orm_mode = True

class CarsResponse(BaseModel):
    cars: List[CarroListing]
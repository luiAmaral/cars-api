from pydantic import BaseModel

class ModeloBase(BaseModel):
    nome: str
    valor_fipe: float
    marca_id: int

class ModeloCreate(ModeloBase):
    pass

class ModeloUpdate(ModeloBase):
    pass

class Modelo(ModeloBase):
    id: int

    class Config:
        orm_mode = True
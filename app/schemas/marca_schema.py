from pydantic import BaseModel

class MarcaBase(BaseModel):
    nome_marca: str

class MarcaCreate(MarcaBase):
    pass

class MarcaUpdate(MarcaBase):
    pass

class Marca(MarcaBase):
    id: int

    class Config:
        orm_mode = True
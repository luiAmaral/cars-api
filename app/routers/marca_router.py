from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import  schemas
from ..services import marca_service as crud
from ..database import SessionLocal

router = APIRouter(
    prefix="/marcas",
    tags=["Marcas"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Marca])
def read_marcas_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    marcas = crud.get_marcas(db, skip=skip, limit=limit)
    return marcas

@router.get("/{marca_id}", response_model=schemas.Marca)
def read_marca_by_id_endpoint(marca_id: int, db: Session = Depends(get_db)):
    db_marca = crud.get_marca(db, marca_id=marca_id)
    if db_marca is None:
        raise HTTPException(status_code=404, detail="Marca não encontrada")
    return db_marca

@router.post("/", response_model=schemas.Marca, status_code=201)
def create_marca_endpoint(marca: schemas.MarcaCreate, db: Session = Depends(get_db)):
    """Cria uma nova marca, verificando se o nome já existe."""
    db_marca = crud.create_marca(db=db, marca=marca)
    
    if db_marca == "nome_existente":
        raise HTTPException(
            status_code=409, 
            detail="Já existe uma marca com este nome."
        )
    
    return db_marca

@router.put("/{marca_id}", response_model=schemas.Marca)
def update_marca_endpoint(marca_id: int, marca: schemas.MarcaUpdate, db: Session = Depends(get_db)):
    """Atualiza os dados de uma marca específica."""
    db_marca = crud.update_marca(db, marca_id=marca_id, marca_update=marca)
    if db_marca is None:
        raise HTTPException(status_code=404, detail="Marca não encontrada")
    
    if db_marca == "nome_existente":
        raise HTTPException(
            status_code=409, 
            detail="Já existe outra marca com este nome.")
    
    return db_marca

@router.delete("/{marca_id}", response_model=schemas.Marca)
def delete_marca_endpoint(marca_id: int, db: Session = Depends(get_db)):
    """Remove uma marca do banco de dados."""
    db_marca = crud.delete_marca(db, marca_id=marca_id)
    
    if db_marca is None:
        raise HTTPException(status_code=404, detail="Marca não encontrada")
    
    if db_marca == "possui_modelos_associados":
        raise HTTPException(
            status_code=409,
            detail="Esta marca não pode ser excluída, pois possui modelos associados. Remova os modelos primeiro."
        )
        
    return db_marca
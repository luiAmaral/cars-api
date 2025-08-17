from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas
from ..services import modelo_service as crud
from ..database import SessionLocal
from typing import List

router = APIRouter(
    prefix="/modelos",
    tags=["Modelos"]
)

# Reutilizando a mesma função de dependência
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.get("/", response_model=List[schemas.Modelo])
def read_modelos_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todos os modelos de carros cadastrados.
    """
    modelos = crud.get_modelos(db, skip=skip, limit=limit)
    return modelos

@router.get("/{modelo_id}", response_model=schemas.Modelo)
def read_modelo_by_id_endpoint(modelo_id: int, db: Session = Depends(get_db)):
    db_modelo = crud.get_modelo(db, modelo_id=modelo_id)
    if db_modelo is None:
        raise HTTPException(status_code=404, detail="Modelo não encontrado")
    return db_modelo

@router.post("/", response_model=schemas.Modelo, status_code=201)
def create_modelo_endpoint(modelo: schemas.ModeloCreate, db: Session = Depends(get_db)):
    db_modelo = crud.create_modelo(db=db, modelo=modelo)
    
    if db_modelo is None:
        raise HTTPException(
            status_code=400,
            detail=f"Marca com ID {modelo.marca_id} não encontrada."
        )
        
    return db_modelo

@router.put("/{modelo_id}", response_model=schemas.Modelo)
def update_modelo_endpoint(modelo_id: int, modelo: schemas.ModeloUpdate, db: Session = Depends(get_db)):
    """Atualiza os dados de um modelo específico."""
    db_modelo = crud.update_modelo(db, modelo_id=modelo_id, modelo_update=modelo)
    
    if db_modelo is None:
        raise HTTPException(status_code=404, detail="Modelo não encontrado")
    
    if db_modelo == "marca_nao_encontrada":
        raise HTTPException(
            status_code=400,
            detail=f"Não foi possível atualizar: Marca com ID {modelo.marca_id} não encontrada."
        )   
    return db_modelo

@router.delete("/{modelo_id}", response_model=schemas.Modelo)
def delete_modelo_endpoint(modelo_id: int, db: Session = Depends(get_db)):
    """Remove um modelo do banco de dados."""
    db_modelo = crud.delete_modelo(db, modelo_id=modelo_id)
    
    if db_modelo is None:
        raise HTTPException(status_code=404, detail="Modelo não encontrado")
    
    if db_modelo == "possui_carros_associados":
        raise HTTPException(
            status_code=409,
            detail="Este modelo não pode ser excluído, pois possui carros associados. Remova os carros primeiro."
        )
        
    return db_modelo

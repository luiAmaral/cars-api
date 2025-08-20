from platform import node
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import null
from sqlalchemy.orm import Session
from .. import  schemas
from ..services import carro_service as crud
from ..database import SessionLocal

router = APIRouter(
    prefix="/cars",  
    tags=["Carros"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=schemas.CarsResponse)
def list_cars_custom_endpoint(db: Session = Depends(get_db)):
    cars_data = crud.get_all_cars_with_details(db)
    return {"cars": cars_data}

@router.get("/{carro_id}", response_model=schemas.Carro)
def read_carro_by_id_endpoint(carro_id: int, db: Session = Depends(get_db)):
    db_carro = crud.get_carro(db, carro_id=carro_id)
    if db_carro is None:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    return db_carro

@router.post("/", response_model=schemas.Carro, status_code=201)
def create_carro_endpoint(carro: schemas.CarroCreate, db: Session = Depends(get_db)):
    db_carro = crud.create_carro(db=db, carro=carro)

    if db_carro is None:
        raise HTTPException(
            status_code=400,
            detail=f"Não foi possível criar o carro: Modelo com ID {carro.modelo_id} não encontrado."
        )

    return db_carro

@router.put("/{carro_id}", response_model=schemas.Carro)
def update_carro_endpoint(carro_id: int, carro: schemas.CarroUpdate, db: Session = Depends(get_db)):
    updated_carro = crud.update_carro(db, carro_id=carro_id, carro_update=carro)
    
    if updated_carro is None:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    
    if updated_carro == "modelo_nao_encontrado":
        raise HTTPException(
            status_code=400,
            detail=f"Não foi possível atualizar: Modelo com ID {carro.modelo_id} não encontrado."
        )
        
    return updated_carro

@router.delete("/{carro_id}", response_model=schemas.Carro)
def delete_carro_endpoint(carro_id: int, db: Session = Depends(get_db)):
    db_carro = crud.delete_carro(db, carro_id=carro_id)
    if db_carro is None:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    return db_carro


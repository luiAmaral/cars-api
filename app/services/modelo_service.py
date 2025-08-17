from sqlalchemy.orm import Session, joinedload
import time
from app import models, schemas

def get_modelos(db: Session, skip: int = 0, limit: int = 100):
    """Busca uma lista de modelos com paginação."""
    return db.query(models.Modelo).offset(skip).limit(limit).all()

def get_modelo(db: Session, modelo_id: int):
    """Busca um único modelo pelo seu ID."""
    return db.query(models.Modelo).filter(models.Modelo.id == modelo_id).first()

def create_modelo(db: Session, modelo: schemas.ModeloCreate):
    """Cria um novo modelo no banco de dados."""
    db_marca = db.query(models.Marca).filter(models.Marca.id == modelo.marca_id).first()
    
    if not db_marca:
        return None
    
    db_modelo = models.Modelo(**modelo.model_dump())
    db.add(db_modelo)
    db.commit()
    db.refresh(db_modelo)
    return db_modelo

def update_modelo(db: Session, modelo_id: int, modelo_update: schemas.ModeloUpdate):
    """Atualiza um modelo existente."""
    db_modelo = get_modelo(db, modelo_id=modelo_id)
    if not db_modelo:
        return None
    
    update_data = modelo_update.model_dump(exclude_unset=True)

    if "marca_id" in update_data:
        db_marca = db.query(models.Marca).filter(models.Marca.id == update_data["marca_id"]).first()
        if not db_marca:
            return "marca_nao_encontrada"

    for key, value in update_data.items():
        setattr(db_modelo, key, value)
        
    db.commit()
    db.refresh(db_modelo)
    return db_modelo

def delete_modelo(db: Session, modelo_id: int):
    """Deleta um modelo, verificando se há carros dependentes."""
    carro_associado = db.query(models.Carro).filter(models.Carro.modelo_id == modelo_id).first()

    if carro_associado:
        return "possui_carros_associados"

    db_modelo = get_modelo(db, modelo_id=modelo_id)
    if not db_modelo:
        return None
        
    db.delete(db_modelo)
    db.commit()
    return db_modelo
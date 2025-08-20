from sqlalchemy.orm import Session
from app import models, schemas

def get_marca_by_name(db: Session, nome_marca: str):
    return db.query(models.Marca).filter(models.Marca.nome_marca == nome_marca).first()


def get_marca(db: Session, marca_id: int):
    return db.query(models.Marca).filter(models.Marca.id == marca_id).first()

def get_marcas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Marca).offset(skip).limit(limit).all()

def create_marca(db: Session, marca: schemas.MarcaCreate):
    db_marca_existente = get_marca_by_name(db, nome_marca=marca.nome_marca)
    if db_marca_existente:
        return "nome_existente"

    db_marca = models.Marca(nome_marca=marca.nome_marca)
    db.add(db_marca)
    db.commit()
    db.refresh(db_marca)
    return db_marca

def update_marca(db: Session, marca_id: int, marca_update: schemas.MarcaUpdate):
    db_marca = get_marca(db, marca_id=marca_id)
    if not db_marca:
        return None
    
    update_data = marca_update.model_dump(exclude_unset=True)

    if "nome_marca" in update_data:
        db_marca_existente = get_marca_by_name(db, nome_marca=update_data["nome_marca"])
        if db_marca_existente and db_marca_existente.id != marca_id:
            return "nome_existente"

    for key, value in update_data.items():
        setattr(db_marca, key, value)
        
    db.commit()
    db.refresh(db_marca)
    return db_marca

def delete_marca(db: Session, marca_id: int):
    modelo_associado = db.query(models.Modelo).filter(models.Modelo.marca_id == marca_id).first()

    if modelo_associado:
        return "possui_modelos_associados"

    db_marca = get_marca(db, marca_id=marca_id)
    if not db_marca:
        return None
        
    db.delete(db_marca)
    db.commit()
    return db_marca
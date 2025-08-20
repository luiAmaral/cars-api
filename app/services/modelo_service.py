from sqlalchemy.orm import Session
from app import models, schemas

def get_modelo_by_name_and_marca(db: Session, nome: str, marca_id: int):
    return db.query(models.Modelo).filter(
        models.Modelo.nome == nome,
        models.Modelo.marca_id == marca_id
    ).first()

def get_modelos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Modelo).offset(skip).limit(limit).all()

def get_modelo(db: Session, modelo_id: int):
    return db.query(models.Modelo).filter(models.Modelo.id == modelo_id).first()

def create_modelo(db: Session, modelo: schemas.ModeloCreate):
    db_marca = db.query(models.Marca).filter(models.Marca.id == modelo.marca_id).first()
    if not db_marca:
        return "marca_nao_encontrada"
    
    db_modelo_existente = get_modelo_by_name_and_marca(db, nome=modelo.nome, marca_id=modelo.marca_id)
    if db_modelo_existente:
        return "nome_existente"
    
    db_modelo = models.Modelo(**modelo.model_dump())
    db.add(db_modelo)
    db.commit()
    db.refresh(db_modelo)
    return db_modelo

def update_modelo(db: Session, modelo_id: int, modelo_update: schemas.ModeloUpdate):
    db_modelo = get_modelo(db, modelo_id=modelo_id)
    if not db_modelo:
        return None
    
    update_data = modelo_update.model_dump(exclude_unset=True)

    if "marca_id" in update_data:
        db_marca = db.query(models.Marca).filter(models.Marca.id == update_data["marca_id"]).first()
        if not db_marca:
            return "marca_nao_encontrada"
            
    if "nome" in update_data:
        marca_id_contexto = update_data.get("marca_id", db_modelo.marca_id)
        db_modelo_existente = get_modelo_by_name_and_marca(db, nome=update_data["nome"], marca_id=marca_id_contexto)
        if db_modelo_existente and db_modelo_existente.id != modelo_id:
            return "nome_existente"

    for key, value in update_data.items():
        setattr(db_modelo, key, value)
        
    db.commit()
    db.refresh(db_modelo)
    return db_modelo

def delete_modelo(db: Session, modelo_id: int):
    carro_associado = db.query(models.Carro).filter(models.Carro.modelo_id == modelo_id).first()

    if carro_associado:
        return "possui_carros_associados"

    db_modelo = get_modelo(db, modelo_id=modelo_id)
    if not db_modelo:
        return None
        
    db.delete(db_modelo)
    db.commit()
    return db_modelo
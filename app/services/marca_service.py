from sqlalchemy.orm import Session, joinedload
import time

from app import models, schemas

def get_marca(db: Session, marca_id: int):
    """Busca uma única marca pelo seu ID."""
    return db.query(models.Marca).filter(models.Marca.id == marca_id).first()

def get_marcas(db: Session, skip: int = 0, limit: int = 100):
    """Busca uma lista de marcas com paginação."""
    return db.query(models.Marca).offset(skip).limit(limit).all()

def create_marca(db: Session, marca: schemas.MarcaCreate):
    """Cria uma nova marca no banco de dados."""
    # Cria um objeto do modelo SQLAlchemy a partir dos dados do schema
    db_marca = models.Marca(nome_marca=marca.nome_marca)
    db.add(db_marca)      # Adiciona o objeto à sessão do banco
    db.commit()           # Confirma (salva) as mudanças no banco
    db.refresh(db_marca)  # Atualiza o objeto com os dados do banco (como o novo id)
    return db_marca

def update_marca(db: Session, marca_id: int, marca_update: schemas.MarcaUpdate):
    """Atualiza uma marca existente."""
    db_marca = get_marca(db, marca_id=marca_id)
    if not db_marca:
        return None
    
    # Pega os dados do schema que foram enviados (excluindo os que não foram setados)
    update_data = marca_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_marca, key, value)
        
    db.commit()
    db.refresh(db_marca)
    return db_marca

def delete_marca(db: Session, marca_id: int):
    """Deleta uma marca, verificando se há modelos dependentes."""
    modelo_associado = db.query(models.Modelo).filter(models.Modelo.marca_id == marca_id).first()

    if modelo_associado:
        return "possui_modelos_associados"

    db_marca = get_marca(db, marca_id=marca_id)
    if not db_marca:
        return None
        
    db.delete(db_marca)
    db.commit()
    return db_marca
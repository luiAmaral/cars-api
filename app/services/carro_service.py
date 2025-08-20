from sqlalchemy.orm import Session, joinedload
import time
from app import models, schemas

def get_all_cars_with_details(db: Session):
    results = db.query(models.Carro).options(joinedload(models.Carro.modelo).joinedload(models.Modelo.marca)).all()
    
    car_list = []
    for carro in results:
        car_data = {
            "id": carro.id,
            "timestamp_cadastro": carro.timestamp_cadastro,
            "modelo_id": carro.modelo_id,
            "ano": carro.ano,
            "combustivel": carro.combustivel,
            "num_portas": carro.num_portas,
            "cor": carro.cor,
            "nome_modelo": carro.modelo.nome,
            "valor": carro.modelo.valor_fipe,
            "brand": carro.modelo.marca.id,
        }
        car_list.append(car_data)
        
    return car_list

def create_carro(db: Session, carro: schemas.CarroCreate):
    db_modelo = db.query(models.Modelo).filter(models.Modelo.id == carro.modelo_id).first()

    if not db_modelo:
        return None

    timestamp = int(time.time())
    db_carro = models.Carro(**carro.model_dump(), timestamp_cadastro=timestamp)
    db.add(db_carro)
    db.commit()
    db.refresh(db_carro)
    return db_carro

def get_carro(db: Session, carro_id: int):
    return db.query(models.Carro).filter(models.Carro.id == carro_id).first()

def update_carro(db: Session, carro_id: int, carro_update: schemas.CarroUpdate):
    db_carro = get_carro(db, carro_id=carro_id)
    if not db_carro:
        return None

    update_data = carro_update.model_dump(exclude_unset=True)

    if "modelo_id" in update_data:
        db_modelo = db.query(models.Modelo).filter(models.Modelo.id == update_data["modelo_id"]).first()
        
        if not db_modelo:
            return "modelo_nao_encontrado"

    for key, value in update_data.items():
        setattr(db_carro, key, value)
        
    db.commit()
    db.refresh(db_carro)
    return db_carro

def delete_carro(db: Session, carro_id: int):
    db_carro = get_carro(db, carro_id=carro_id)
    if not db_carro:
        return None
    db.delete(db_carro)
    db.commit()
    return db_carro
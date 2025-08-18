from sqlalchemy.orm import Session, joinedload
import time
from app import models, schemas

def get_all_cars_with_details(db: Session):
    """
    Busca todos os carros e faz um JOIN com a tabela de modelos
    para montar a resposta customizada exigida no desafio.
    """
    # .options(joinedload(models.Carro.modelo)) é uma otimização.
    # Ele diz ao SQLAlchemy para fazer um JOIN e carregar os dados do modelo
    # relacionado na mesma query, evitando múltiplas consultas ao banco (problema N+1).
    results = db.query(models.Carro).options(joinedload(models.Carro.modelo).joinedload(models.Modelo.marca)).all()
    
    # Agora, vamos transformar os resultados para que correspondam ao schema CarroListing.
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
            "nome_modelo": carro.modelo.nome,  # Pega o nome do modelo relacionado
            "valor": carro.modelo.valor_fipe,   # Pega o valor do modelo relacionado
            "brand": carro.modelo.marca.id,
        }
        car_list.append(car_data)
        
    return car_list

def create_carro(db: Session, carro: schemas.CarroCreate):
    """Cria um novo carro no banco de dados, validando o modelo_id."""
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
    """Busca um único carro pelo seu ID."""
    return db.query(models.Carro).filter(models.Carro.id == carro_id).first()

def update_carro(db: Session, carro_id: int, carro_update: schemas.CarroUpdate):
    """Atualiza um carro existente, validando o novo modelo_id se fornecido."""
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
    """Deleta um carro."""
    db_carro = get_carro(db, carro_id=carro_id)
    if not db_carro:
        return None
    db.delete(db_carro)
    db.commit()
    return db_carro
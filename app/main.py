from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app import models 
from .routers import marca_router, modelo_router, carro_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WS Work Car API",
    description="API para o desafio de backend da WS Work.",
    version="1.0.0"
)

origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(marca_router.router)
app.include_router(modelo_router.router)
app.include_router(carro_router.router)

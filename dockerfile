# Use uma imagem oficial do Python
FROM python:3.10-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo de dependências e instale
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da sua aplicação
COPY . .

# Comando para iniciar sua aplicação com Uvicorn
# Substitua 'main:app' pelo nome do arquivo python principal e a instância do FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
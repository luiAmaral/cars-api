# CAR API

Esta é a API de back-end para o sistema de gerenciamento de carros do desafio da WS WORK.

## Pré-requisitos

- Python 3.10 ou superior
- Um servidor de banco de dados MySQL

## Como Rodar o Projeto

1.  **Clone o repositório:**

2.  **Crie e ative um ambiente virtual:**

    # Windows
    python -m venv venv
    .\venv\Scripts\Activate

    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate


3.  **Instale as dependências:**
    pip install -r requirements.txt

4.  **Configure as variáveis de ambiente:**
    - Copie o arquivo de exemplo: `cp .env.example .env`
    - Edite o arquivo `.env` e adicione suas credenciais do banco de dados.

5.  **Execute a aplicação:**
    uvicorn app.main:app --reload

A API estará disponível em `http://127.0.0.1:8000`.


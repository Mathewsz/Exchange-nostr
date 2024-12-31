#!/bin/bash

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Para Unix/macOS
# venv\Scripts\activate   # Para Windows

# Instalar dependências
pip install -r backend/requirements.txt

# Inicializar banco de dados
python -c "from backend.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Iniciar servidor
uvicorn backend.main:app --reload

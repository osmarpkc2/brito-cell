#!/bin/bash

# Cria diretórios necessários
mkdir -p static/images/products

# Configura permissões
chmod -R 755 static

# Instala dependências
pip install -r requirements.txt

# Cria o banco de dados
python -c "from app import app, db; app.app_context().push(); db.create_all()"

#!/bin/bash

# Cria diretórios necessários
mkdir -p static/images/products

# Instala dependências
pip install -r requirements-vercel.txt

# Cria um arquivo config.json padrão se não existir
if [ ! -f "config.json" ]; then
    echo '{
        "admin_credentials": {
            "username": "admin",
            "password": "@IsaaciphonesBC2025"
        },
        "secret_key": "@IsaaciphonesBC2025",
        "upload_folder": "static/images/products"
    }' > config.json
fi

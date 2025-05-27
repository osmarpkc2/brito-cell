#!/bin/bash

# Configuração de cores para mensagens
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para exibir mensagens de sucesso
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Função para exibir avisos
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Função para exibir erros e sair
error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

echo -e "${GREEN}🚀 Iniciando o processo de build...${NC}"

# Instala as dependências do Python
warning "Instalando dependências do Python..."
pip install -r requirements-vercel.txt || error "Falha ao instalar as dependências do Python"

# Cria diretórios necessários
warning "Criando diretórios necessários..."
mkdir -p static/images/products
mkdir -p static/css
mkdir -p static/js
mkdir -p logs

# Configura permissões
warning "Configurando permissões..."
chmod -R 755 static
chmod -R 755 logs

# Configura o ambiente
export FLASK_APP=app.py
export FLASK_ENV=production

# Verifica se o PostgreSQL está configurado
if [ -n "$POSTGRES_URL" ] || [ -n "$DATABASE_URL" ]; then
    success "Usando banco de dados PostgreSQL..."
    # Configura a URL do banco de dados para o PostgreSQL
    if [ -z "$DATABASE_URL" ] && [ -n "$POSTGRES_URL" ]; then
        export DATABASE_URL=$POSTGRES_URL
    fi
    
    # Instala o psycopg2 para PostgreSQL
    warning "Instalando psycopg2 para PostgreSQL..."
    pip install psycopg2-binary || warning "Falha ao instalar psycopg2, continuando sem ele..."
else
    warning "Usando SQLite como banco de dados..."
    export DATABASE_URL="sqlite:////tmp/britocell.db"
fi

# Inicializa o banco de dados
warning "Inicializando banco de dados..."
python -c "
import os
import sys
from app import app, db

try:
    with app.app_context():
        db.create_all()
        print('✅ Banco de dados inicializado com sucesso!')
        sys.exit(0)
except Exception as e:
    print(f'❌ Erro ao inicializar o banco de dados: {str(e)}')
    sys.exit(1)
" || error "Falha ao inicializar o banco de dados"

# Gera arquivos estáticos se necessário
warning "Verificando arquivos estáticos..."
if [ ! -f "static/css/style.css" ]; then
    warning "Arquivo CSS não encontrado, criando um vazio..."
    touch static/css/style.css
fi

if [ ! -f "static/js/main.js" ]; then
    warning "Arquivo JavaScript não encontrado, criando um vazio..."
    echo "// Arquivo JavaScript principal" > static/js/main.js
fi

# Verifica se o diretório de uploads existe
if [ ! -d "static/images/products" ]; then
    warning "Diretório de uploads não encontrado, criando..."
    mkdir -p static/images/products
fi

# Cria um arquivo .gitkeep vazio se não existir
if [ ! -f "static/images/products/.gitkeep" ]; then
    touch static/images/products/.gitkeep
fi

# Verifica se o arquivo de banco de dados SQLite existe
if [[ "$DATABASE_URL" == *"sqlite:///"* ]]; then
    DB_FILE="${DATABASE_URL/sqlite:\/\//}"
    if [ ! -f "$DB_FILE" ]; then
        warning "Arquivo de banco de dados SQLite não encontrado, será criado automaticamente."
    fi
fi

success "✅ Build concluído com sucesso!"
exit 0

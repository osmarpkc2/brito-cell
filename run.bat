@echo off
set FLASK_APP=app.py
set FLASK_ENV=development

:: Verifica se o ambiente virtual existe, se não, cria
if not exist "venv\" (
    echo Criando ambiente virtual...
    python -m venv venv
    call venv\Scripts\activate
    echo Instalando dependências...
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

echo Iniciando o servidor...
python -m flask run --host=0.0.0.0 --port=5000
pause

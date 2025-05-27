import os
import sys

# Adiciona o diretório raiz ao path
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_path)

# Configura o ambiente
os.environ['FLASK_APP'] = 'app:app'
os.environ['FLASK_ENV'] = 'production'

# Importa o aplicativo Flask
from app import app as application

# Configura o aplicativo para usar os diretórios corretos
application.static_folder = os.path.join(root_path, 'static')
application.template_folder = os.path.join(root_path, 'templates')

# Cria diretórios necessários
os.makedirs(application.static_folder, exist_ok=True)
os.makedirs(os.path.join(application.static_folder, 'images', 'products'), exist_ok=True)

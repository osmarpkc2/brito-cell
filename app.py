from flask import Flask, render_template, redirect, url_for, flash, request, abort, Blueprint, current_app, json, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from functools import wraps
import hashlib
import json
from werkzeug.utils import secure_filename
import sys

# Carrega as configurações
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Cria um arquivo de configuração padrão se não existir
        config = {
            "admin_credentials": {
                "username": "admin",
                "password": "@IsaaciphonesBC2025"  # Será substituído por hash
            },
            "secret_key": "sua-chave-secreta-aqui",
            "upload_folder": "static/images/products"
        }
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        return config

# Carrega as configurações
config = load_config()

# Atualiza a senha para hash se ainda estiver em texto plano
if not config['admin_credentials']['password'].startswith('pbkdf2:'):
    from werkzeug.security import generate_password_hash
    config['admin_credentials']['password'] = generate_password_hash(config['admin_credentials']['password'])
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

# Cria o blueprint principal
main_bp = Blueprint('main', __name__)

# Cria a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua-chave-secreta-padrao')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images', 'products')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Garante que o diretório de upload existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'main.admin_login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'

# Modelo de usuário
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

# Carrega o usuário admin do arquivo de configuração
admin_creds = config['admin_credentials']
admin_user = User(id=1, username=admin_creds['username'], password_hash=admin_creds['password'])

@login_manager.user_loader
def load_user(user_id):
    if int(user_id) == 1:  # ID 1 é o admin
        return admin_user
    return None

# Dados em memória (substitui o banco de dados)
products = [
    {
        'id': 1,
        'name': 'iPhone 15 Pro Max',
        'description': 'O mais avançado iPhone com câmera profissional e tela Super Retina XDR.',
        'price': 8999.90,
        'stock': 10,
        'color': 'black',
        'storage': '256GB',
        'image_url': 'https://images.unsplash.com/photo-1697898706717-858403a390ac?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
        'created_at': datetime.now(timezone.utc)
    },
    {
        'id': 2,
        'name': 'iPhone 14 Pro',
        'description': 'Câmera avançada, chip A16 Bionic e tela Super Retina XDR.',
        'price': 7599.90,
        'stock': 5,
        'color': 'silver',
        'storage': '128GB',
        'image_url': 'https://images.unsplash.com/photo-1673505566097-5d8a75a2f602d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
        'created_at': datetime.now(timezone.utc)
    },
    {
        'id': 3,
        'name': 'iPhone 13',
        'description': 'Sistema de câmera avançado, chip A15 Bionic e bateria que dura o dia todo.',
        'price': 4999.90,
        'stock': 3,
        'color': 'blue',
        'storage': '128GB',
        'image_url': 'https://images.unsplash.com/photo-1632660678308-393e2d0e2b8d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
        'created_at': datetime.now(timezone.utc)
    }
]

def create_app():
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()
    
    # Cria a aplicação Flask
    app = Flask(__name__)
    
    # Configurações da aplicação
    app.config['SECRET_KEY'] = config.get('secret_key', os.getenv('SECRET_KEY', 'dev-key-change-in-production'))
    app.config['UPLOAD_FOLDER'] = config.get('upload_folder', os.path.join('static', 'images', 'products'))
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Configura o caminho para a pasta de templates
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app.template_folder = template_dir
    
    # Inicializa o Flask-Login
    login_manager.init_app(app)
    
    # Registra o blueprint principal
    app.register_blueprint(main_bp)
    
    return app

# Função para obter um produto por ID
def get_product(product_id):
    for product in products:
        if product['id'] == product_id:
            return product
    return None

# Rota para a página inicial
@main_bp.route('/')
def index():
    return render_template('main/index.html', products=products)

# Rota para a página de detalhes do produto
@main_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = get_product(product_id)
    if not product:
        abort(404)
    return render_template('main/product_detail.html', product=product)

# Adiciona a data atual e funções auxiliares ao contexto de todos os templates
@main_bp.context_processor
def inject_globals():
    def get_product_image_url(product):
        """Retorna a URL da imagem do produto, com fallback para imagem padrão se necessário."""
        if product.get('image'):
            return url_for('static', filename=product['image'])
        elif product.get('image_url'):
            return product['image_url']
        return 'https://via.placeholder.com/300x300/CCCCCC/999999?text=Sem+Imagem'
    
    def get_color_code(color_name):
        """Retorna o código hexadecimal da cor baseado no nome em português."""
        color_map = {
            'preto': '#000000',
            'branco': '#FFFFFF',
            'prata': '#C0C0C0',
            'dourado': '#FFD700',
            'azul': '#0000FF',
            'vermelho': '#FF0000',
            'verde': '#008000',
            'amarelo': '#FFFF00',
            'roxo': '#800080',
            'rosa': '#FFC0CB',
            'cinza': '#808080',
            'azul marinho': '#000080',
            'verde água': '#00FFFF',
            'laranja': '#FFA500',
            'marrom': '#A52A2A',
            'ouro rosa': '#E0BFB8'
        }
        # Remove acentos e converte para minúsculas
        color_name = ''.join(char for char in color_name.lower() if char.isalpha() or char.isspace())
        return color_map.get(color_name, '#CCCCCC')  # Retorna cinza claro se a cor não for encontrada
    
    return {
        'now': datetime.now(timezone.utc),
        'get_product_image_url': get_product_image_url,
        'get_color_code': get_color_code
    }



# Rota para o painel de administração
@main_bp.route('/admin')
@login_required
def admin_dashboard():
    # Ordena os produtos pelo ID em ordem decrescente (mais recentes primeiro)
    sorted_products = sorted(products, key=lambda x: x['id'], reverse=True)
    return render_template('admin/dashboard.html', products=sorted_products)

# Rota para login do administrador
@main_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Verifica as credenciais
        if username == admin_user.username and admin_user.check_password(password):
            login_user(admin_user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.admin_dashboard'))
        
        flash('Usuário ou senha inválidos', 'danger')
    
    return render_template('admin/login.html')

# Rota para logout do administrador
@main_bp.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('main.index'))

# Rota para adicionar um novo produto
@main_bp.route('/admin/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if request.method == 'POST':
        # Cria um novo produto com os dados do formulário
        new_id = max([p['id'] for p in products]) + 1 if products else 1
        
        new_product = {
            'id': new_id,
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'price': float(request.form.get('price', 0)),
            'stock': int(request.form.get('stock', 0)),
            'color': request.form.get('color', 'black'),
            'storage': request.form.get('storage', '128GB'),
            'image_url': request.form.get('image_url', ''),
            'created_at': datetime.now(timezone.utc)
        }
        
        products.append(new_product)
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    
    # Se for GET, exibe o formulário de cadastro
    return render_template('admin/product_form.html', product=None)

# Rota para editar um produto existente
@main_bp.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        flash('Produto não encontrado!', 'danger')
        return redirect(url_for('main.admin_dashboard'))
    
    if request.method == 'POST':
        # Atualiza os dados do produto
        product['name'] = request.form.get('name', product['name'])
        product['description'] = request.form.get('description', product['description'])
        product['price'] = float(request.form.get('price', product['price']))
        product['stock'] = int(request.form.get('stock', product['stock']))
        product['color'] = request.form.get('color', product['color'])
        product['storage'] = request.form.get('storage', product['storage'])
        product['image_url'] = request.form.get('image_url', product.get('image_url', ''))
        
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    
    # Se for GET, exibe o formulário de edição
    return render_template('admin/product_form.html', product=product)

# Rota para excluir um produto
@main_bp.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    global products
    product = next((p for p in products if p['id'] == product_id), None)
    
    if not product:
        flash('Produto não encontrado!', 'danger')
    else:
        products = [p for p in products if p['id'] != product_id]
        flash('Produto excluído com sucesso!', 'success')
    
    return redirect(url_for('main.admin_dashboard'))

# Registra os blueprints
app.register_blueprint(main_bp)

# Configura o LoginManager
login_manager.init_app(app)

# Adiciona o filtro ao ambiente do Jinja2
app.jinja_env.filters['format_currency'] = lambda value: f'R$ {value:,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.')

# Verifica se o arquivo está sendo executado diretamente
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

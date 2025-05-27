from flask import Flask, render_template, redirect, url_for, flash, request, abort, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.urls import url_decode
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from functools import wraps

# Inicializa as extensões
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Cria o blueprint principal
main_bp = Blueprint('main', __name__)

def create_app():
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()
    
    # Cria a aplicação Flask
    app = Flask(__name__)
    
    # Configurações da aplicação
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///britocell.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images', 'products')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Configura o caminho para a pasta de templates
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app.template_folder = template_dir
    
    # Garante que a pasta de uploads existe
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Inicializa as extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.admin_login'  # Atualizado para usar o nome do blueprint
    
    # Registra o blueprint principal
    app.register_blueprint(main_bp)
    
    # Cria o contexto da aplicação para poder acessar o app dentro das funções
    with app.app_context():
        db.create_all()
        # Inicializa o banco de dados se necessário
        init_db(app)
    
    return app

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String(200))  # Caminho para imagem salva localmente
    image_url = db.Column(db.String(500))  # URL para imagem externa
    color = db.Column(db.String(50), nullable=False, default='Preto')
    storage = db.Column(db.String(50), nullable=False, default='128GB')

# Função auxiliar para verificar se um arquivo tem uma extensão permitida
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Função para carregar o usuário pelo ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Função para salvar um produto
def save_product(product, form_data, files, app):
    try:
        product.name = form_data.get('name')
        product.description = form_data.get('description')
        product.price = float(form_data.get('price', 0))
        product.stock = int(form_data.get('stock', 0))
        product.color = form_data.get('color', 'Preto')
        product.storage = form_data.get('storage', '128GB')
        
        # Processa o upload da imagem, se houver
        if 'image' in files:
            file = files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                product.image = filename
                product.image_url = None  # Limpa a URL se um arquivo foi enviado
        
        # Se não houver arquivo, verifica se há uma URL de imagem
        elif form_data.get('image_url'):
            product.image_url = form_data.get('image_url')
            product.image = None  # Limpa a imagem se uma URL foi fornecida
        
        db.session.add(product)
        db.session.commit()
        return True, "Produto salvo com sucesso!"
    except Exception as e:
        db.session.rollback()
        return False, f"Erro ao salvar o produto: {str(e)}"

# Função para inicializar o banco de dados
def init_db(app):
    with app.app_context():
        # Verifica se já existe um usuário admin
        if not User.query.filter_by(username='admin').first():
            # Cria o usuário admin com senha 'admin123'
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123', method='pbkdf2:sha256')
            )
            db.session.add(admin)
            try:
                db.session.commit()
                print('Usuário admin criado com sucesso!')
            except Exception as e:
                db.session.rollback()
                print(f'Erro ao criar usuário admin: {str(e)}')
        else:
            print("Usuário admin já existe.")

# Rota para a página inicial
@main_bp.route('/')
def index():
    products = Product.query.all()
    return render_template('main/index.html', products=products)

# Adiciona a data atual ao contexto de todos os templates
@main_bp.context_processor
def inject_now():
    return {'now': datetime.now(timezone.utc).astimezone()}

# Rota para o painel de administração
@main_bp.route('/admin')
@login_required
def admin_dashboard():
    products = Product.query.all()
    return render_template('admin/dashboard.html', products=products)

# Rota para login do administrador
@main_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.admin_dashboard'))
        
        flash('Usuário ou senha inválidos', 'error')
    
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
        product = Product()
        success, message = save_product(product, request.form, request.files, current_app)
        if success:
            flash('Produto adicionado com sucesso!', 'success')
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash(message, 'error')
    
    return render_template('admin/product_form.html', product=None)

# Rota para editar um produto existente
@main_bp.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        success, message = save_product(product, request.form, request.files, current_app)
        if success:
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash(message, 'error')
    
    return render_template('admin/product_form.html', product=product)

# Rota para excluir um produto
@main_bp.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    try:
        # Remove a imagem do produto se existir
        if product.image:
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], product.image)
            if os.path.exists(image_path):
                os.remove(image_path)
        
        db.session.delete(product)
        db.session.commit()
        flash('Produto excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir o produto: {str(e)}', 'error')
    
    return redirect(url_for('main.admin_dashboard'))

# Verifica se o arquivo está sendo executado diretamente
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

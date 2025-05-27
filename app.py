from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.urls import url_decode
import os
from datetime import datetime
from dotenv import load_dotenv
from functools import wraps

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Adiciona contexto global para todos os templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///britocell.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images', 'products')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'

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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('main/index.html', products=products)

@app.route('/admin')
@login_required
def admin_dashboard():
    products = Product.query.all()
    return render_template('admin/dashboard.html', products=products)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Usuário ou senha inválidos')
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

def save_product(product, form_data, files):
    """Helper function to save product data"""
    product.name = form_data.get('name')
    product.description = form_data.get('description')
    product.price = float(form_data.get('price'))
    product.stock = int(form_data.get('stock'))
    product.color = form_data.get('color')
    
    # Get image URL from form if provided
    image_url = form_data.get('image_url', '').strip()
    
    # Handle file upload (takes precedence over URL if both are provided)
    image_file = files.get('image')
    if image_file and image_file.filename:  # If a new file was uploaded
        if not allowed_file(image_file.filename):
            flash('Tipo de arquivo não permitido. Use apenas JPG, PNG ou GIF.', 'error')
            return None
            
        # Remove old image if exists
        if product.image:
            try:
                old_image_path = os.path.join(app.static_folder, product.image)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            except Exception as e:
                app.logger.error(f'Erro ao remover imagem antiga: {e}')
        
        # Save new image
        filename = secure_filename(image_file.filename)
        image_filename = os.path.join('images', 'products', filename)
        os.makedirs(os.path.dirname(os.path.join(app.static_folder, image_filename)), exist_ok=True)
        image_file.save(os.path.join(app.static_folder, image_filename))
        
        # Update product with new image and clear URL
        product.image = image_filename
        product.image_url = None
    elif image_url:  # If URL was provided
        # Clear the uploaded image if switching to URL
        if product.image:
            try:
                old_image_path = os.path.join(app.static_folder, product.image)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            except Exception as e:
                app.logger.error(f'Erro ao remover imagem antiga: {e}')
            product.image = None
        
        # Update product with new URL
        product.image_url = image_url
    # If neither file nor URL is provided and it's a new product, show error
    elif not product.id:  # New product must have either image or URL
        flash('Por favor, envie uma imagem ou forneça uma URL de imagem.', 'error')
        return None
    
    # If it's an edit and no new image/URL was provided, keep the existing one
    
    db.session.add(product)
    db.session.commit()
    return product

@app.route('/admin/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if request.method == 'POST':
        product = Product()
        save_product(product, request.form, request.files)
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/product_form.html', product=None)

@app.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        save_product(product, request.form, request.files)
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/product_form.html', product=product)

@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Remove the image file if it exists
    if product.image:
        try:
            image_path = os.path.join(app.static_folder, product.image)
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            app.logger.error(f'Error removing product image: {e}')
    
    db.session.delete(product)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('admin_dashboard'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Função para criar o banco de dados e o usuário admin
def init_db():
    with app.app_context():
        db.create_all()
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()

# Inicializa o banco de dados quando o aplicativo for iniciado
init_db()

# Este bloco só será executado quando o arquivo for executado diretamente
if __name__ == '__main__':
    app.run(debug=True)

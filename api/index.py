import os
import sys
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# Adiciona o diretório raiz ao path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

# Configura o ambiente
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'production'
os.environ['PYTHONUNBUFFERED'] = '1'

# Instala as dependências necessárias
os.system('pip install -r requirements-vercel.txt')

# Importa o aplicativo Flask
from app import app as application

# Configura o aplicativo para usar o diretório estático corretamente
application.static_folder = os.path.join(root_path, 'static')
application.static_url_path = '/static'

# Configura o caminho para os templates
application.template_folder = os.path.join(root_path, 'templates')

def handler(event, context):
    """
    Handler para o Vercel Serverless Functions
    """
    try:
        from vercel_python.wsgi import VercelWSGIHandler
        return VercelWSGIHandler(application).handle(event, context)
    except Exception as e:
        # Log do erro para depuração
        print(f"Erro no handler: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': f'Erro interno do servidor: {str(e)}',
            'headers': {'Content-Type': 'text/plain'}
        }

# Configuração para desenvolvimento local
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port, debug=True)

"""
AVISO: ESTE CÓDIGO FOI GERADO POR INTELIGÊNCIA ARTIFICIAL (Claude 3.7 Sonnet)
NÃO FOI ESCRITO MANUALMENTE PELO AUTOR DO REPOSITÓRIO
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa as extensões
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Cria e configura a aplicação Flask
    app = Flask(__name__)
    
    # Configurações da aplicação
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'uma_chave_secreta_padrao')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql://root:password@localhost/celpip_trainer')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa as extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registra os blueprints
    from app.routes import main, admin, evaluator, applicant
    app.register_blueprint(main.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(evaluator.bp)
    app.register_blueprint(applicant.bp)
    
    return app 
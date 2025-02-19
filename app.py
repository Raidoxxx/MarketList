# app.py (por exemplo)
from flask import Flask, render_template
from flask_login import LoginManager
from models.Base import Base, engine, SessionLocal
from models.User import User
from controllers.user_controller import user_bp
from controllers.item_controller import item_bp
from controllers.list_controller import list_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'sua_chave_secreta_aqui'  # Idealmente, use uma variável de ambiente

    # Configura Flask-Login
    login_manager = LoginManager(app)
    login_manager.login_view = 'user_bp.login'

    @login_manager.user_loader
    def load_user(user_id):
        with SessionLocal() as session:
            user = session.query(User).filter_by(id=user_id).first()
            return user

    # Registra blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(list_bp)

    # Cria as tabelas (ou use migrações, ver abaixo)
    Base.metadata.create_all(bind=engine)

    @app.route('/')
    def home():
        # Como retornar para o arquivo HTML?
        return render_template('index.html')
    return app

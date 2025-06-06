from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, url_for
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('app.config.Config')

# Configurações do banco de dados (exemplo com SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configurações de e-mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'seu_email@gmail.com'  # Seu Gmail
app.config['MAIL_PASSWORD'] = 'senha_de_app_gerada'  # Não é sua senha normal!
app.config['MAIL_DEFAULT_SENDER'] = 'seu_email@gmail.com'
app.config['ADMIN_EMAIL'] = 'seu_email@gmail.com'

mail = Mail(app)

from app.controllers.auth_controller import AuthController
from app.controllers.dashboard_controller import DashboardController

app.register_blueprint(AuthController)
app.register_blueprint(DashboardController)

def create_app():
    return app

@app.route('/')
def index():
    return redirect(url_for('auth.login'))
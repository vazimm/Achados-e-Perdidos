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
app.config['MAIL_SERVER'] = 'smtp.office365.com'                # ou outro servidor SMTP
app.config['MAIL_PORT'] = 587                               # porta para TLS
app.config['MAIL_USERNAME'] = 'achados_e_perdidos_u@hotmail.com'         # seu e-mail
app.config['MAIL_PASSWORD'] = '!hol00ew-perdidos2s61a%'                   # sua senha ou app password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'achados_e_perdidos_u@hotmail.com'   # remetente padrão
# Endereço administrativo que receberá os e-mails
app.config['ADMIN_EMAIL'] = 'achados_e_perdidos_u@hotmail.com'

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
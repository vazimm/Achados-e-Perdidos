from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, url_for

app = Flask(__name__)
app.config.from_object('app.config.Config')

db = SQLAlchemy(app)

from app.controllers.auth_controller import AuthController
from app.controllers.dashboard_controller import DashboardController

app.register_blueprint(AuthController)
app.register_blueprint(DashboardController)

def create_app():
    return app

@app.route('/')
def index():
    return redirect(url_for('auth.login'))
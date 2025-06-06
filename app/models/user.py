from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)  # nova coluna para nome
    email = db.Column(db.String(120), unique=True, nullable=False)
    #notifications_count = db.Column(db.Integer, default=0) Imcompleto
    password = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'admin' ou 'user'
    cep = db.Column(db.String(8), nullable=True)            # RA para alunos
    date_of_birth = db.Column(db.Date, nullable=True)
    cpf = db.Column(db.String(14), unique=True, nullable=True)  # Formato: 000.000.000-00

    def __init__(self, name, email, password, user_type, cep, date_of_birth, cpf):
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type
        self.cep = cep
        self.date_of_birth = date_of_birth
        self.cpf = cpf

    def __repr__(self):
        return f'<User {self.email}>'

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
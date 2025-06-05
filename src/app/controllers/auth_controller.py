from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from app.models.user import User
from app import db
from datetime import date

AuthController = Blueprint('auth', __name__, url_prefix='/auth')

@AuthController.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['senha']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_type'] = user.user_type
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('dashboard.user_dashboard' if user.user_type == 'user' else 'dashboard.admin_dashboard'))
        else:
            flash('Email ou senha inválidos.', 'danger')
    return render_template('auth/login.html')

@AuthController.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['senha']
        name = request.form['name']  # novo campo
        cep = request.form['cep']
        # Converte a data recebida (formato: YYYY-MM-DD) para objeto date
        data_nascimento_str = request.form['dataNascimento']
        data_nascimento = date.fromisoformat(data_nascimento_str)
        cpf = request.form['cpf']
        new_user = User(
            email=email,
            password=password,
            user_type='user',
            name=name,  # adicionado
            cep=cep,
            date_of_birth=data_nascimento,
            cpf=cpf
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registro bem-sucedido! Você pode fazer login agora.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')
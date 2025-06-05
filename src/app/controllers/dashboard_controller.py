from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from app.models.user import User
from datetime import date
from app import db

DashboardController = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@DashboardController.route('/user')
def user_dashboard():
    if 'user_id' not in session:
        flash('Faça login para acessar o dashboard!', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
   
    return render_template('dashboard/user_dashboard.html', user=user)

@DashboardController.route('/admin')
def admin_dashboard():
    if 'user_id' not in session:
        flash('Faça login para acessar o dashboard!', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    if user.user_type != 'admin':
        return redirect(url_for('dashboard.user_dashboard'))
    
    return render_template('dashboard/admin_dashboard.html', user=user)


@DashboardController.route('/admin/new_item', methods=['GET', 'POST'])
def new_item():
    if 'user_id' not in session:
        flash('Faça login para acessar o dashboard!', 'warning')
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if user.user_type != 'admin':
        flash('Acesso restrito.', 'warning')
        return redirect(url_for('dashboard.user_dashboard'))
    
    if request.method == 'POST':
        # Lógica para processar o cadastro do novo item
        flash('Item cadastrado com sucesso!', 'success')
        return redirect(url_for('dashboard.admin_dashboard'))
    
    return render_template('dashboard/new_item.html')

@DashboardController.route('/recuperar_pertence')
def recuperar_pertence():
    # Renderiza o template que exibe o formulário
    return render_template('dashboard/recuperar_pertence.html')


@DashboardController.route('/submit-request-item', methods=['POST'])
def submit_request_item():
    # Aqui você pode processar a solicitação de recuperação do objeto
    # Exemplo de processamento:
    flash('Solicitação enviada com sucesso!', 'success')
    return redirect(url_for('dashboard.user_dashboard'))
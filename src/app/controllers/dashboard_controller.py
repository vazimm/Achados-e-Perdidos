from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from app.models.user import User
from app.models.item import Item  # Importa o modelo Item
from app import db
import datetime  # Importa o módulo datetime

DashboardController = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# Rota de dashboard do usuário
@DashboardController.route('/user')
def user_dashboard():
    # Verifica se o usuário está logado (sessão iniciada)
    if 'user_id' not in session:
        flash('Faça login para acessar o dashboard!', 'warning')
        return redirect(url_for('auth.login'))
    
    # Busca o usuário atual a partir da sessão
    user = User.query.get(session['user_id'])
    # Renderiza o template do dashboard do usuário, passando o usuário
    return render_template('dashboard/user_dashboard.html', user=user)

#Rota de dashboard de admin
@DashboardController.route('/admin')
def admin_dashboard():
    # Verifica se o usuário está logado
    if 'user_id' not in session:
        flash('Faça login para acessar o dashboard!', 'warning')
        return redirect(url_for('auth.login'))
    
    # Busca o usuário atual
    user = User.query.get(session['user_id'])
    # Caso o usuário não seja admin, redireciona para o dashboard de usuário
    if user.user_type != 'admin':
        return redirect(url_for('dashboard.user_dashboard'))
    
    # Renderiza o template do dashboard de admin, passando o usuário
    return render_template('dashboard/admin_dashboard.html', user=user)

#Novo item
@DashboardController.route('/admin/new_item', methods=['GET', 'POST'])
def new_item():
    # Verifica se o usuário está logado
    if 'user_id' not in session:
        flash('Faça login para acessar o dashboard!', 'warning')
        return redirect(url_for('auth.login'))

    # Busca o usuário atual
    user = User.query.get(session['user_id'])
    # Caso o usuário não seja admin, exibe acesso restrito e redireciona
    if user.user_type != 'admin':
        flash('Acesso restrito.', 'warning')
        return redirect(url_for('dashboard.user_dashboard'))
    
    if request.method == 'POST':
        # Coleta os dados do formulário
        item_date_str = request.form.get('item_date')  # Ex: '2025-06-06'
        item_time_str = request.form.get('item_encontrado_time')  # Ex: '14:30'
        funcionario = request.form.get('funcionario')
        local = request.form.get('local')
        item_description = request.form.get('item_description')

        # Converte as strings para tipos apropriados
        try:
            date_obj = datetime.datetime.strptime(item_date_str, '%Y-%m-%d').date()
            time_obj = datetime.datetime.strptime(item_time_str, '%H:%M').time()
        except ValueError:
            flash('Formato de data ou hora inválido.', 'danger')
            return redirect(url_for('dashboard.new_item'))

        # Cria uma instância de Item utilizando os dados do formulário
        new_item_record = Item(
            item_date=date_obj,
            item_encontrado_time=time_obj,
            funcionario=funcionario,
            local=local,
            item_description=item_description
        )
        # Adiciona o item na sessão e commita no banco de dados
        db.session.add(new_item_record)
        db.session.commit()

        flash('Item cadastrado com sucesso!', 'success')
        return redirect(url_for('dashboard.admin_dashboard'))
    
    # Se o método for GET, renderiza o template para cadastro do novo item
    return render_template('dashboard/new_item.html')

@DashboardController.route('/recuperar_pertence')
def recuperar_pertence():
    # Busca todos os items registrados no banco de dados
    items = Item.query.all()
    # Renderiza o template e passa a lista de items
    return render_template('dashboard/recuperar_pertence.html', items=items)

@DashboardController.route('/submit-request-item', methods=['POST'])
def submit_request_item():
    # Lógica para processar a solicitação de recuperação do objeto
    # Após o processamento, exibe mensagem de sucesso e redireciona para o dashboard do usuário
    flash('Solicitação enviada com sucesso!', 'success')
    return redirect(url_for('dashboard.user_dashboard'))
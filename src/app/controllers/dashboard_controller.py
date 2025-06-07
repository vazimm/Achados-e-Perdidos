import os
from flask import Blueprint, render_template, redirect, url_for, session, flash, request, current_app
from app.models.user import User
from app.models.item import Item  # Importa o modelo Item
from werkzeug.utils import secure_filename
from app import db, mail  # Certifique-se de que mail é a instância do Flask-Mail
import datetime
from flask_mail import Message

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        item_date_str = request.form.get('item_date')
        item_time_str = request.form.get('item_encontrado_time')
        funcionario = request.form.get('funcionario')
        local = request.form.get('local')
        item_description = request.form.get('item_description')

        try:
            date_obj = datetime.datetime.strptime(item_date_str, '%Y-%m-%d').date()
            time_obj = datetime.datetime.strptime(item_time_str, '%H:%M').time()
        except ValueError:
            flash('Formato de data ou hora inválido.', 'danger')
            return redirect(url_for('dashboard.new_item'))

        # Upload de imagem
        imagem_file = request.files.get('imagem')
        imagem_path = None

        if imagem_file and allowed_file(imagem_file.filename):
            filename = secure_filename(imagem_file.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            full_path = os.path.join(upload_folder, filename)
            imagem_file.save(full_path)
            imagem_path = os.path.join('uploads', filename).replace('\\', '/')  # Garante que o caminho seja relativo e use barras corretas

        new_item_record = Item(
            item_date=date_obj,
            item_encontrado_time=time_obj,
            funcionario=funcionario,
            local=local,
            item_description=item_description,
            imagem_path=imagem_path
        )

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
    # Verifica se o usuário está logado
    if 'user_id' not in session:
        flash('Faça login para acessar o dashboard!', 'warning')
        return redirect(url_for('auth.login'))
    
    # Recupera o usuário atual
    user = User.query.get(session['user_id'])
    
    # Recupera o ID do item a partir do formulário
    item_id = request.form.get('item_id')
    if not item_id:
        flash("Item não especificado.", "danger")
        return redirect(url_for('dashboard.recuperar_pertence'))
    
    # Busca o item no banco de dados
    item = Item.query.get(item_id)
    if not item:
        flash("Item não encontrado.", "danger")
        return redirect(url_for('dashboard.recuperar_pertence'))
    
    # Monta a mensagem de e-mail utilizando os dados do item e do usuário em sessão
    msg = Message(
        subject="Solicitação de recuperação de item",
        sender=current_app.config.get('MAIL_DEFAULT_SENDER'),  # Pode ser ajustado conforme a política do servidor de e-mails
        recipients=[current_app.config.get('ADMIN_EMAIL')]  # Endereço administrativo configurado na aplicação
    )
    
    msg.body = f"""
Email: {user.email}
Nome: {user.name}

Assunto: Recuperar item

ID do item: {item.id}
Data que foi encontrado: {item.item_date.strftime('%Y-%m-%d')}
Horário: {item.item_encontrado_time.strftime('%H:%M')}
Funcionário: {item.funcionario}
Descrição: {item.item_description}
"""
    # Envia o e-mail
    mail.send(msg)
    
    flash("Solicitação enviada com sucesso!", "success")
    return redirect(url_for('dashboard.user_dashboard'))
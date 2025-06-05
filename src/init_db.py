from app import app, db
from app.models.user import User
from datetime import date

with app.app_context():
    # Cria todas as tabelas definidas nos modelos
    db.create_all()
    print("Tabelas criadas com sucesso!")
    
    # Configuração do usuário admin (caso não exista)
    admin_email = "admin@exemplo.com"
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            email=admin_email,
            password="",
            user_type="admin",
            name="Administrador",
            cep="",
            date_of_birth=None,
            cpf=""
        )
        # Defina uma senha padrão para o admin (alterar conforme necessário)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Usuário admin criado com sucesso!")
    else:
        print("Usuário admin já existe!")
    
    # Configuração do usuário de exemplo (caso não exista)
    example_email = "user@exemplo.com"
    example_user = User.query.filter_by(email=example_email).first()
    if not example_user:
        example_user = User(
            email=example_email,
            password="",
            user_type="user",
            name="Usuário Exemplo",
            cep="00000000",
            date_of_birth=date(2000, 1, 1),
            cpf="00000000000"
        )
        example_user.set_password("user123")
        db.session.add(example_user)
        db.session.commit()
        print("Usuário de exemplo criado com sucesso!")
    else:
        print("Usuário de exemplo já existe!")
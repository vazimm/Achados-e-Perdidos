# Projeto Achados e Perdidos

Este é um projeto web desenvolvido em Flask para gerenciamento de itens perdidos e encontrados. O sistema possui funcionalidades para cadastro de usuários, login, gerenciamento de itens (para admin e usuários) e solicitação de recuperação dos pertences.

## Estrutura do Projeto

O projeto está organizado da seguinte maneira:

```
c:\Users\username\Documents\Projetos\A3 em Grupo\Achados e Perdidos\src
│
├── .gitignore
├── create_db.py             # Script para criação do banco de dados e tabelas
├── init_db.py               # Inicializa o banco de dados com dados padrão (admin e usuário de exemplo)
├── requirements.txt         # Dependências do projeto
├── run.py                   # Arquivo principal para iniciar a aplicação Flask
│
├── app/
│   ├── __init__.py          # Configura a aplicação Flask e registra os Blueprints
│   ├── config.py            # Configurações da aplicação (secret key, URL do BD etc.)
│   ├── controllers/         # Controladores (rotas e lógica de aplicação)
│   │   ├── auth_controller.py
│   │   └── dashboard_controller.py
│   ├── models/              # Modelos de dados (por exemplo, o modelo de usuário)
│   │   └── user.py
│   └── templates/           # Templates HTML
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       └── dashboard/
│           ├── admin_dashboard.html
│           ├── new_item.html
│           ├── recuperar_pertence.html
│           └── user_dashboard.html
│
└── app/static/              # Arquivos estáticos (CSS, imagens, etc.)
    ├── css/
    │   ├── style_admin.css
    │   ├── style_login.css
    │   ├── style_request.css
    │   └── style_user.css
    └── images/
        └── (imagens usadas no projeto, por exemplo, Brasão_BH.png, background.jpg)
```

## Funcionalidades

- **Autenticação:**  
  - Cadastro de novos usuários (rota `/auth/register`)  
  - Login de usuários (rota `/auth/login`)  

- **Dashboard:**  
  - Painel para usuários com cards informativos e funcionalidades de recuperação de itens.  
  - Painel para administradores para gerenciamento de itens e usuários.

- **Recuperação de Pertences:**  
  - Tela para solicitação de recuperação de um item (`/dashboard/recuperar_pertence`)  
  - Processamento da solicitação via rota POST (`/dashboard/submit-request-item`)

## Estilização

O projeto utiliza CSS para aplicar um visual consistente:

- **Background:**  
  Todas as telas possuem um background definido por uma imagem padrão, com o estilo aplicado via `background-size: cover`.

- **Cards e Containers:**  
  Os cards (em `style_user.css` e `style_admin.css`) utilizam um fundo semi-transparente com efeito de _blur_ (`backdrop-filter: blur(10px)`), bordas arredondadas e sombras.

- **Formulários:**  
  Os formulários (em `style_login.css` e `style_request.css`) seguem o padrão de cores com elementos de entrada (inputs, selects, e buttons) combinados com um esquema de cores que garante contraste (texto escuro e fundo claro para os campos).

## Configuração e Execução

1. **Instalar Dependências:**  
   Certifique-se de ter o Python instalado e execute:
   ```bash
   pip install -r requirements.txt
   ```

2. **Criar o Banco de Dados:**  
   Utilize o script de inicialização:
   ```bash
   python init_db.py
   ```
   ou
   ```bash
   python create_db.py
   ```

3. **Rodar a Aplicação:**  
   Inicie o servidor Flask com:
   ```bash
   python run.py
   ```
   A aplicação estará disponível em `http://127.0.0.1:5000/`.

## Estrutura dos Blueprints

- **AuthController:**  
  Localizado em `app/controllers/auth_controller.py`, gerencia as rotas de login e registro.

- **DashboardController:**  
  Localizado em `app/controllers/dashboard_controller.py`, gerencia as rotas do painel de administração e usuário, incluindo as rotas para cadastro de novo item e solicitação de recuperação de pertences.

## Contribuição

Contribuições são bem-vindas! Se desejar melhorar o projeto, sinta-se à vontade para criar sugestões ou abrir _pull requests_.

## Licença

Este projeto é destinado para fins educacionais. Sinta-se livre para adaptá-lo conforme necessário.

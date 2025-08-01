from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, Usuario, Modulo, Tarefa
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from app import db
from flask_login import LoginManager, login_user, logout_user
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)   # → gera uma chave segura
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"  # Redireciona para /login se não autenticado
login_manager.login_message_category = "info"

#Quem for pegar o projeto, poe em comentario e faz a sua rota do bdd, e so troca quem fica comentado ou nao

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass123@localhost:3306/Aurum' #Local Banco Tarifa
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://estudante1:senhaaalterar@localhost:3306/Aurum' #Local IFSP
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass123@localhost:3306/Aurum' #Local banco Silva
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#print("Conectando ao banco em:", os.environ.get("DATABASE_URL"))



db.init_app(app)

with app.app_context():
    db.create_all()

# 🔐 Página de Login
@app.route("/login")
def login_page():
    return render_template("login.html")

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
    
@app.route("/debug-db")
def debug_db():
    return f"Usando URI: {app.config['SQLALCHEMY_DATABASE_URI']}"

# Página do questionário de entrada
@app.route("/questionario")
@login_required
def questionario_page():
    return render_template("perguntasEntrada.html")

# 🆕 Página de Cadastro
@app.route("/cadastro")
def cadastro_page():
    return render_template("cadastro.html")


# 🏆 Página de Ranking
@app.route("/ranking")
@login_required
def ranking_page():
    return render_template("ranking.html")


# 🏆 Página de Ranking semanal
@app.route("/inicial")
@login_required
def starting_page():
    return render_template("a.html")

# 🏆 Página de Quando Inicia o Sistema
@app.route("/")
def presentation_page():
    return render_template("Aurum.html")

@app.route("/pre-entrada")
@login_required
def pre_entrada():
    return render_template("preentrada.html")

@app.route("/perfil")
@login_required
def perfil_page():
    return render_template("perfil.html", usuario=current_user)

@app.route("/modulo")
@login_required
def modulo():
    return render_template("modulos.html")

@app.route("/introducao")
@login_required
def intro_page():
    return render_template("introducao.html")

@app.route("/cadastro", methods=["POST"])
def cadastro():
    dados = request.json
    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")
    print(nome, email, senha)
    if not nome or not email or not senha:
        return jsonify({"mensagem": "Por favor, preencha todos os campos."}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"mensagem": "E-mail já cadastrado."}), 400

    senha_hash = generate_password_hash(senha)

    novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"mensagem": f"Usuário {nome} cadastrado com sucesso!"})


@app.route("/quiz")
@login_required
def quiz_page():
    return render_template("quizes.html")

@app.route("/loja")
@login_required
def store_page():
    return render_template("loja.html")

@app.route("/login", methods=["POST"])
def efetuar_login():
    dados = request.get_json()
    email_ou_nome = dados.get("emailOuNome")
    senha = dados.get("senha")

    if not email_ou_nome or not senha:
        return jsonify({"mensagem": "Preencha todos os campos."}), 400
    
    usuario = Usuario.query.filter(
        (Usuario.email == email_ou_nome) | (Usuario.nome == email_ou_nome)
    ).first()

    if usuario and check_password_hash(usuario.senha, senha):
        login_user(usuario)  # ← faz o login real do usuário
        return jsonify({"mensagem": "Login efetuado com sucesso!"}), 200
    else:
        return jsonify({"mensagem": "Email/nome ou senha incorretos."}), 401

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("login_page"))    

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/atualizar_perfil', methods=['POST'])
@login_required
def atualizar_perfil():
    nome = request.form['apelido']
    foto = request.files['foto_perfil']
    usuario = get_usuario_atual()  # ← substitua com sua lógica

    if foto and allowed_file(foto.filename):
        filename = secure_filename(f"{usuario.id}_{foto.filename}")
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        filepath = caminho.removeprefix("static/")
        foto.save(caminho)
        usuario.profilepicture = filepath  # Salva no banco o caminho do arquivo

    usuario.nome = nome
    salvar_usuario(usuario)  # Atualiza o banco com os dados

    flash('Perfil atualizado com sucesso!')
    return redirect(url_for('perfil_page'))

def get_usuario_atual():
    return current_user

def salvar_usuario(nome):
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Erro ao salvar no banco:", e)
        raise

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}


if __name__ == "__main__":
    app.run(debug=True)
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host="0.0.0.0", port=port)

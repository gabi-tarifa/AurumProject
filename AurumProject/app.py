from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, Usuario, Modulo, Tarefa, Conquistas, UsuarioConquistas, Poderes, PoderesUsuario
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from app import db
from flask_login import LoginManager, login_user, logout_user
import secrets
from setup_conquistas import criar_conquistas
from setup_poderes import criar_poderes
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)   # → gera uma chave segura
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"  # Redireciona para /login se não autenticado
login_manager.login_message_category = "info"

#Quem for pegar o projeto, poe em comentario e faz a sua rota do bdd, e so troca quem fica comentado ou nao

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Rayquaza%201@localhost:3306/Aurum' #Local Banco Silva
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://estudante1:senhaaalterar@localhost:3306/Aurum' #Local IFSP
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass123@localhost:3306/Aurum' #Banco Local Tarifa
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL") #Banco Deploy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#print("Conectando ao banco em:", os.environ.get("DATABASE_URL"))



db.init_app(app)

with app.app_context():
    db.create_all()
    criar_conquistas()
    criar_poderes()



def zerar_pontos_semanais():
    with app.app_context():  # Necessário para acessar o banco
        Usuario.query.update({Usuario.pontos_semanais: 0})
        db.session.commit()
        print(f"Pontos semanais resetados em {datetime.now()}")

scheduler = BackgroundScheduler()
# Executa todo domingo às 00:00
scheduler.add_job(zerar_pontos_semanais, 'cron', day_of_week='sun', hour=0, minute=0)
scheduler.start()

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
    usuarios = Usuario.query.order_by(Usuario.pontos_semanais.desc()).all()

    # Encontrar a posição do usuário no ranking
    posicao_ranking = next((i + 1 for i, u in enumerate(usuarios) if u.id == current_user.id), None)

    return render_template(
        "ranking.html",
        usuario=current_user,
        usuarios=usuarios,
        posicao_ranking=posicao_ranking,
        pontos = current_user.pontos,
        pontos_semanais=current_user.pontos_semanais,
        coins=current_user.moedas  # Ou current_user.coins, se esse for o nome
    )

# 🏆 Página de Ranking semanal
@app.route("/inicial")
@login_required
def starting_page():
    usuarios = Usuario.query.order_by(Usuario.pontos_semanais.desc()).all()

    # Encontrar a posição do usuário no ranking
    posicao_ranking = next((i + 1 for i, u in enumerate(usuarios) if u.id == current_user.id), None)

    return render_template(
        "a.html",
        usuario=current_user,
        usuarios=usuarios,
        posicao_ranking=posicao_ranking,
        pontos=current_user.pontos,
        pontos_semanais=current_user.pontos_semanais,
        coins=current_user.moedas  # Ou current_user.coins, se esse for o nome
    )

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
    conquistas_usuario = db.session.query(Conquistas).join(UsuarioConquistas).filter(UsuarioConquistas.id_usuario == current_user.id).all()
    usuarios = Usuario.query.order_by(Usuario.pontos_semanais.desc()).all()

    # Encontrar a posição do usuário no ranking
    posicao_ranking = next((i + 1 for i, u in enumerate(usuarios) if u.id == current_user.id), None)

    return render_template(
        "perfil.html",
        usuario=current_user,
        conquistas=conquistas_usuario,
        usuarios=usuarios,
        posicao_ranking=posicao_ranking,
        pontos = current_user.pontos,
        pontos_semanais=current_user.pontos_semanais,
        coins=current_user.moedas  # Ou current_user.coins, se esse for o nome
    )

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
    usuarios = Usuario.query.order_by(Usuario.pontos_semanais.desc()).all()

    # Encontrar a posição do usuário no ranking
    posicao_ranking = next((i + 1 for i, u in enumerate(usuarios) if u.id == current_user.id), None)

    return render_template(
        "quizes.html",
        usuario=current_user,
        usuarios=usuarios,
        posicao_ranking=posicao_ranking,
        pontos = current_user.pontos,
        pontos_semanais=current_user.pontos_semanais,
        coins=current_user.moedas  # Ou current_user.coins, se esse for o nome
    )

@app.route("/loja")
@login_required
def store_page():
    usuarios = Usuario.query.order_by(Usuario.pontos_semanais.desc()).all()
    
    poderes = Poderes.query.all()

    # Encontrar a posição do usuário no ranking
    posicao_ranking = next((i + 1 for i, u in enumerate(usuarios) if u.id == current_user.id), None)
    

    return render_template(
        "loja.html",
        usuario=current_user,
        poderes=poderes,
        usuarios=usuarios,
        posicao_ranking=posicao_ranking,
        pontos = current_user.pontos,
        pontos_semanais=current_user.pontos_semanais,
        coins=current_user.moedas  # Ou current_user.coins, se esse for o nome
    )


@app.route("/comprar_poder", methods=["POST"])
@login_required
def comprar_poder():
    poder_id = request.form.get("poder_id")
    poder = Poderes.query.get(poder_id)

    if not poder:
        flash("Poder não encontrado.", "error")
        return redirect(url_for("store_page"))

    # Verifica saldo
    if current_user.coins < poder.preco:
        flash("Você não tem moedas suficientes.", "error")
        return redirect(url_for("store_page"))

    # Cria relacionamento no PoderesUsuario
    compra = PoderesUsuario(usuario_id=current_user.id, poder_id=poder.id_poder)
    db.session.add(compra)

    # Desconta moedas
    current_user.coins -= poder.preco
    db.session.commit()

    flash(f"Você comprou '{poder.nome}'!", "success")
    return redirect(url_for("store_page"))

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
    
@app.route("/testar_conquistas")
@login_required
def testar_conquistas():
    conquistas_a_dar = ["Eu SOU um OG", "Vencedor", "Aurum Master", "Campeão Invicto"]
    
    for nome in conquistas_a_dar:
        conquista = Conquistas.query.filter_by(nome=nome).first()
        if conquista:
            desbloquear_conquista(current_user.id, conquista.id_conquista)

    return redirect(url_for("perfil_page"))
    
@app.route("/eusouOG")
@login_required
def eusouOG():
    conquistas_a_dar = ["Eu SOU um OG"]
    
    for nome in conquistas_a_dar:
        conquista = Conquistas.query.filter_by(nome=nome).first()
        if conquista:
            desbloquear_conquista(current_user.id, conquista.id_conquista)

    return redirect(url_for("perfil_page"))
    
@app.route("/ifsp413")
@login_required
def ifiano413():
    conquistas_a_dar = ["Farinha do Mesmo Saco"]
    
    for nome in conquistas_a_dar:
        conquista = Conquistas.query.filter_by(nome=nome).first()
        if conquista:
            desbloquear_conquista(current_user.id, conquista.id_conquista)

    return redirect(url_for("perfil_page"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("login_page"))    

UPLOAD_FOLDER = 'static/uploads/'
UPLOADBG_FOLDER = 'static/uploadsBG/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOADBG_FOLDER'] = UPLOADBG_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/atualizar_perfil', methods=['POST'])
@login_required
def atualizar_perfil():
    nome = request.form['apelido']
    foto = request.files['foto_perfil']
    fundo = request.files['foto_fundo']
    usuario = get_usuario_atual()

    if foto and allowed_file(foto.filename):
        filename = secure_filename(f"{usuario.id}_{foto.filename}")
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        filepath = caminho.removeprefix("static/")
        foto.save(caminho)
        usuario.profilepicture = filepath  # Salva no banco o caminho do arquivo
    
    if fundo and allowed_file(fundo.filename):
        filename_fundo = secure_filename(f"{usuario.id}_fundo_{fundo.filename}")
        caminho_fundo = os.path.join(app.config['UPLOADBG_FOLDER'], filename_fundo)
        filepathbg = caminho_fundo.removeprefix("static/")
        fundo.save(caminho_fundo)
        usuario.backgroundpicture = filepathbg  # ← nova coluna

    usuario.nome = nome
    salvar_usuario(usuario)  # Atualiza o banco com os dados

    flash('Perfil atualizado com sucesso!')
    return redirect(url_for('perfil_page'))

def get_usuario_atual():
    return current_user

def desbloquear_conquista(id_usuario, id_conquista):
    ja_tem = UsuarioConquistas.query.filter_by(id_usuario=id_usuario, id_conquista=id_conquista).first()
    if not ja_tem:
        nova = UsuarioConquistas(id_usuario=id_usuario, id_conquista=id_conquista)
        db.session.add(nova)
        db.session.commit()

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
    #app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

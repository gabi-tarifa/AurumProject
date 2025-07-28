from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, Usuario, Modulo, Tarefa
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass123@localhost:3306/Aurum'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#print("Conectando ao banco em:", os.environ.get("DATABASE_URL"))



db.init_app(app)

with app.app_context():
    db.create_all()

# 🔐 Página de Login
@app.route("/login")
def login_page():
    return render_template("login.html")
    
@app.route("/debug-db")
def debug_db():
    return f"Usando URI: {app.config['SQLALCHEMY_DATABASE_URI']}"

# Página do questionário de entrada
@app.route("/questionario")
def questionario_page():
    return render_template("perguntasEntrada.html")

# 🆕 Página de Cadastro
@app.route("/cadastro")
def cadastro_page():
    return render_template("cadastro.html")


# 🏆 Página de Ranking
@app.route("/ranking")
def ranking_page():
    return render_template("ranking.html")


# 🏆 Página de Ranking semanal
@app.route("/inicial")
def starting_page():
    return render_template("a.html")

# 🏆 Página de Quando Inicia o Sistema
@app.route("/")
def presentation_page():
    return render_template("Aurum.html")

@app.route("/perfil")
def perfil_page():
    return render_template("perfil.html")

@app.route("/modulo")
def modulo():
    return render_template("modulos.html")

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
def quiz_page():
    return render_template("quizes.html")

@app.route("/loja")
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
        return jsonify({"mensagem": "Login efetuado com sucesso!"}), 200
    else:
        return jsonify({"mensagem": "Email/nome ou senha incorretos."}), 401


if __name__ == "__main__":
    app.run(debug=True)
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host="0.0.0.0", port=port)

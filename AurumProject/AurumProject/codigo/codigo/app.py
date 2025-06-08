from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, Usuario
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Rayquaza%201@localhost:3306/Aurum'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

with app.app_context():
    db.create_all()

# 🔐 Página de Login
@app.route("/login")
def login_page():
    return render_template("login.html")


# 🆕 Página de Cadastro
@app.route("/cadastro_page")
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

# 🏆 Página de Ranking semanal
@app.route("/apresentacao")
def presentation_page():
    return render_template("Aurum.html")

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
    print ("funciona")
    app.run(debug=True)

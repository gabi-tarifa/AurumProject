from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, Usuario, Modulo, Tarefa, Conquistas, UsuarioConquistas, Poderes
from models import Ofensiva, PoderesUsuario, Bloco, UsuarioBloco, TarefaUsuario, ConteudoTarefa
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
from datetime import datetime, timedelta, date, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import desc
from flask_babel import Babel, _, format_datetime
from setup_modulos import criar_modulos
from setup_tarefas import criar_tarefas
from setup_conteudo import criar_conteudo
from flask_mail import Mail, Message
import random, string

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

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "grupomoneto2025@gmail.com"
app.config['MAIL_PASSWORD'] = "nzstkfupqrjdyoun"
app.config['MAIL_DEFAULT_SENDER'] = ("Suporte Aurum", "grupomoneto2025@gmail.com")
mail = Mail(app)


app.config["BABEL_DEFAULT_LOCALE"] = "pt"
app.config["BABEL_SUPPORTED_LOCALES"] = ["pt", "en"]
app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations"

db.init_app(app)

with app.app_context():
    db.create_all()
    criar_conquistas()
    criar_poderes()
    criar_modulos()
    criar_tarefas()
    criar_conteudo()

def verificar_bonus_semana():
    with app.app_context():
        usuarios = Usuario.query.all()

        for user in usuarios:
            ofensiva = Ofensiva.query.filter_by(id_usuario=user.id).first()

            if not ofensiva:
                continue  # usuário ainda não começou ofensiva

            if ofensiva.semanal >= 7:
                user.moedas += 50
                print(f"Usuário {user.id} recebeu 50 moedas pela ofensiva semanal!")
            else:
                print(f"Usuário {user.id} não completou a ofensiva semanal.")

            # Resetar a contagem semanal sempre
            ofensiva.dias_semana = [False]*7

        db.session.commit()  # um único commit para todos
# Babel
babel = Babel()
def select_locale():
    # usa o idioma salvo no usuário; se não autenticado, usa padrão
    if current_user.is_authenticated and current_user.idioma:
        return current_user.idioma
    return request.accept_languages.best_match(['pt', 'en'])

babel.init_app(app, locale_selector=select_locale)

def zerar_pontos_semanais():
    with app.app_context():  # Necessário para acessar o banco
        Usuario.query.update({Usuario.pontos_semanais: 0})
        db.session.commit()
        print(f"Pontos semanais resetados em {datetime.now()}")

def distribuir_recompensas(usuarios):
    recompensas = [70, 55, 45, 40, 40, 30, 30, 30, 30, 30,
                   20, 20, 20, 20, 20, 10, 10, 10, 10, 10]

    for i, usuario in enumerate(usuarios[:len(recompensas)]):
        usuario.moedas += recompensas[i]

        # Campeão (só o primeiro de cada bloco)
        if i == 0:
            desbloquear_conquista(usuario.id, "Vencedor") 

def processar_premiacoes():
    # semana "ativa" que está terminando agora
    semana_terminando = inicio_semana()  

    # pega todos os blocos da semana que está acabando
    blocos = Bloco.query.filter(Bloco.semana == semana_terminando).all()

    for bloco in blocos:
        usuarios_bloco = (
            UsuarioBloco.query
            .filter_by(id_bloco=bloco.id_bloco)
            .join(Usuario, Usuario.id == UsuarioBloco.id_usuario)
            .all()
        )

        # transformar em lista de usuários reais
        usuarios = [Usuario.query.get(ub.id_usuario) for ub in usuarios_bloco]

        # ordenar por pontuação
        usuarios.sort(key=lambda u: u.pontos, reverse=True)

        if usuarios:
            distribuir_recompensas(usuarios)

    db.session.commit()

scheduler = BackgroundScheduler()
# Executa toda segunda-feira às 00:00
scheduler.add_job(zerar_pontos_semanais, 'cron', day_of_week='mon', hour=0, minute=0)
scheduler.add_job(verificar_bonus_semana, 'cron', day_of_week='mon', hour=0, minute=0)
scheduler.add_job(processar_premiacoes, 'cron', day_of_week='mon', hour=11, minute=39)
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

# Pagina de Configuracoes
@app.route("/config")
@login_required
def configuracoes():
    # idiomas visíveis no select
    idiomas = [
        {"code": "pt", "name": "Português"},
        {"code": "en", "name": "English"}
    ]
    return render_template("configuracoes.html", idiomas=idiomas, idioma = current_user.idioma)

@app.route("/api/idioma", methods=["POST"])
@login_required
def api_idioma():
    data = request.get_json(silent=True) or request.form
    novo = (data.get("idioma") or "").strip()
    if novo not in app.config["BABEL_SUPPORTED_LOCALES"]:
        return jsonify({"ok": False, "msg": _("Idioma inválido.")}), 400
    current_user.idioma = novo
    db.session.commit()
    # Dica: poderíamos retornar JSON e o front recarregar a página
    return jsonify({"ok": True, "msg": _("Idioma atualizado para %(lang)s.", lang=novo)})

# Pagina de Ajuda
@app.route("/ajuda")
@login_required
def ajuda():
    return render_template("ajuda.html")

@app.route("/modulo_<int:id_modulo>/tarefa_<int:id_tarefa>")
@login_required
def licoes(id_tarefa, id_modulo):
    tarefa = Tarefa.query.filter_by(id_modulo=id_modulo, id_tarefa=id_tarefa).first()
    blocos = []

    for c in tarefa.conteudos:
        if c.tipo == "texto":
            blocos.append({
                "tipo": "texto",
                "conteudo": c.conteudo
            })
        elif c.tipo == "quiz":
            alternativas = []
            if c.alternativas:
                opcoes = c.alternativas.split("||")
                for idx, opcao in enumerate(opcoes, start=1):
                    alternativas.append({
                        "texto": opcao.strip(),
                        "correta": (idx == c.correta)
                    })
            blocos.append({
                "tipo": "quiz",
                "pergunta": c.pergunta,
                "alternativas": alternativas
            })

    return render_template("licoes.html", tarefa=tarefa, blocos_json=blocos, id_tarefa=tarefa.id_tarefa)

# 🆕 Página de Cadastro
@app.route("/cadastro")
def cadastro_page():
    return render_template("cadastro.html")

# 🏆 Página de Ranking
@app.route("/ranking")
@login_required
def ranking_page():
    usuarios = Usuario.query.order_by(Usuario.pontos_semanais.desc()).all()

    semana_atual = inicio_semana()

    bloco_usuario = (UsuarioBloco.query
        .join(Bloco)
        .filter(UsuarioBloco.id_usuario == current_user.id,
                Bloco.semana == semana_atual)
        .first())

    if not bloco_usuario:
        flash("Você ainda não está em um bloco esta semana.", "error")
        return redirect(url_for("dashboard"))

    ranking = (Usuario.query
        .join(UsuarioBloco)
        .filter(UsuarioBloco.id_bloco == bloco_usuario.id_bloco)
        .order_by(Usuario.pontos_semanais.desc())
        .all())

    # Encontrar a posição do usuário no ranking
    posicao_ranking = next((i + 1 for i, u in enumerate(usuarios) if u.id == current_user.id), None)
    
    ofensiva = get_or_create_ofensiva(current_user.id)
    
    # Pega o horário atual em UTC, com timezone explícito
    agora = datetime.now().weekday()

    # Descobre o dia da semana (0 = segunda, 6 = domingo)
    dia_semana = agora


    return render_template(
        "ranking.html",
        usuario=current_user,
        usuarios=usuarios,
        posicao_ranking=posicao_ranking,
        pontos = current_user.pontos,
        pontos_semanais=current_user.pontos_semanais,
        ofensiva=ofensiva,
        dia_semana=dia_semana,
        ranking=ranking,
        coins=current_user.moedas  # Ou current_user.coins, se esse for o nome
    )

# 🏆 Página de Ranking semanal
@app.route("/inicial")
@login_required
def starting_page():
    current_user.ja_passou_intro = True
    db.session.commit()
    usuarios = Usuario.query.order_by(Usuario.pontos_semanais.desc()).all()

    semana_atual = inicio_semana()

    bloco_usuario = (UsuarioBloco.query
        .join(Bloco)
        .filter(UsuarioBloco.id_usuario == current_user.id,
                Bloco.semana == semana_atual)
        .first())

    if not bloco_usuario:
        flash("Você ainda não está em um bloco esta semana.", "error")
        return redirect(url_for("dashboard"))

    ranking = (Usuario.query
        .join(UsuarioBloco)
        .filter(UsuarioBloco.id_bloco == bloco_usuario.id_bloco)
        .order_by(Usuario.pontos_semanais.desc())
        .all())

    # Encontrar a posição do usuário no ranking
    posicao_ranking = next((i + 1 for i, u in enumerate(ranking) if u.id == current_user.id), None)

    # Busca o registro UsuarioBloco do usuário logado
    usuario_blocos = UsuarioBloco.query.filter_by(id_usuario=current_user.id).all()
    usuario_bloco = usuario_blocos[-1] if usuario_blocos else None

    if not usuario_bloco:
        top5_bloco = []  # Usuário não está em bloco
    else:
        id_bloco = usuario_bloco.id_bloco
        top5_bloco = (
            db.session.query(Usuario)
            .join(UsuarioBloco, Usuario.id == UsuarioBloco.id_usuario)
            .filter(UsuarioBloco.id_bloco == id_bloco)
            .order_by(desc(Usuario.pontos_semanais))
            .limit(5)
            .all()
        )

    # 🔹 Agora os módulos + progresso (com bloqueio sequencial)
    modulos = Modulo.query.order_by(Modulo.id).all()
    modulos_progresso = []

    for i, modulo in enumerate(modulos):
        # Total de tarefas do módulo
        tarefas = Tarefa.query.filter_by(id_modulo=modulo.id).all()
        tarefas_totais = len(tarefas)

        # Tarefas concluídas pelo usuário
        tarefas_feitas = (TarefaUsuario.query
            .filter(TarefaUsuario.id_usuario == current_user.id,
                    TarefaUsuario.id_tarefa.in_([t.id_tarefa for t in tarefas]),
                    TarefaUsuario.concluida == True)
            .count())

        # Verifica se o módulo foi concluído
        concluido = tarefas_totais > 0 and tarefas_feitas == tarefas_totais

        # Bloqueia se não for o primeiro módulo e o anterior não estiver concluído
        bloqueado = False
        if i > 0:
            modulo_anterior = modulos_progresso[i-1]
            if not modulo_anterior["concluido"]:
                bloqueado = True

        # Adiciona ao progresso
        modulos_progresso.append({
            "id": modulo.id,
            "nome": modulo.nome,
            "descricao": modulo.descricao,
            "tarefas_feitas": tarefas_feitas,
            "tarefas_totais": tarefas_totais,
            "progresso": (tarefas_feitas / tarefas_totais * 100) if tarefas_totais > 0 else 0,
            "concluido": concluido,
            "bloqueado": bloqueado
        })

        
    ofensiva = get_or_create_ofensiva(current_user.id)
    
    # Pega o horário atual em UTC, com timezone explícito
    agora = datetime.now().weekday()

    # Descobre o dia da semana (0 = segunda, 6 = domingo)
    dia_semana = agora


    return render_template(
        "a.html",
        usuario=current_user,
        usuarios=usuarios,
        posicao_ranking=posicao_ranking,
        top5_bloco=top5_bloco,
        ranking=ranking,
        pontos=current_user.pontos,
        pontos_semanais=current_user.pontos_semanais,
        coins=current_user.moedas,
        ofensiva=ofensiva,
        dia_semana=dia_semana,
        modulos=modulos_progresso
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

    ofensiva = get_or_create_ofensiva(current_user.id)
    
    # Pega o horário atual em UTC, com timezone explícito
    agora = datetime.now().weekday()

    # Descobre o dia da semana (0 = segunda, 6 = domingo)
    dia_semana = agora

    semana_atual = inicio_semana()

    bloco_usuario = (UsuarioBloco.query
        .join(Bloco)
        .filter(UsuarioBloco.id_usuario == current_user.id,
                Bloco.semana == semana_atual)
        .first())

    if not bloco_usuario:
        flash("Você ainda não está em um bloco esta semana.", "error")
        return redirect(url_for("dashboard"))

    ranking = (Usuario.query
        .join(UsuarioBloco)
        .filter(UsuarioBloco.id_bloco == bloco_usuario.id_bloco)
        .order_by(Usuario.pontos_semanais.desc())
        .all())
    
    
    # Busca o registro UsuarioBloco do usuário logado
    usuario_blocos = UsuarioBloco.query.filter_by(id_usuario=current_user.id).all()
    usuario_bloco = usuario_blocos[-1] if usuario_blocos else None

    if not usuario_bloco:
        top5_bloco = []  # Usuário não está em bloco
    else:
        id_bloco = usuario_bloco.id_bloco

    top5_bloco = (
        db.session.query(Usuario)
        .join(UsuarioBloco, Usuario.id == UsuarioBloco.id_usuario)
        .filter(UsuarioBloco.id_bloco == id_bloco)
        .order_by(desc(Usuario.pontos_semanais))
        .limit(5)
        .all()
    )

    # Encontrar a posição do usuário no ranking
    posicao_ranking = next((i + 1 for i, u in enumerate(ranking) if u.id == current_user.id), None)

    return render_template(
        "perfil.html",
        usuario=current_user,
        conquistas=conquistas_usuario,
        usuarios=usuarios,
        ranking=ranking,
        top5_bloco=top5_bloco,
        posicao_ranking=posicao_ranking,
        pontos = current_user.pontos,
        pontos_semanais=current_user.pontos_semanais,
        ofensiva=ofensiva,
        dia_semana=dia_semana,
        coins=current_user.moedas  # Ou current_user.coins, se esse for o nome
    )
@app.route("/modulo_<int:id_modulo>")
@login_required
def ver_modulo(id_modulo):

    semana_atual = inicio_semana()

    bloco_usuario = (UsuarioBloco.query
        .join(Bloco)
        .filter(UsuarioBloco.id_usuario == current_user.id,
                Bloco.semana == semana_atual)
        .first())

    if not bloco_usuario:
        flash("Você ainda não está em um bloco esta semana.", "error")
        return redirect(url_for("dashboard"))

    ranking = (Usuario.query
        .join(UsuarioBloco)
        .filter(UsuarioBloco.id_bloco == bloco_usuario.id_bloco)
        .order_by(Usuario.pontos_semanais.desc())
        .all())
    
    
    # Busca o registro UsuarioBloco do usuário logado
    usuario_blocos = UsuarioBloco.query.filter_by(id_usuario=current_user.id).all()
    usuario_bloco = usuario_blocos[-1] if usuario_blocos else None

    if not usuario_bloco:
        top5_bloco = []  # Usuário não está em bloco
    else:
        id_bloco = usuario_bloco.id_bloco

    top5_bloco = (
        db.session.query(Usuario)
        .join(UsuarioBloco, Usuario.id == UsuarioBloco.id_usuario)
        .filter(UsuarioBloco.id_bloco == id_bloco)
        .order_by(desc(Usuario.pontos_semanais))
        .limit(5)
        .all()
    )
    
    # Encontrar a posição do usuário no ranking
    posicao_ranking = next((i + 1 for i, u in enumerate(ranking) if u.id == current_user.id), None)

    # todas as tarefas do módulo
    tarefas = Tarefa.query.filter_by(id_modulo=id_modulo).order_by(Tarefa.id_tarefa).all()

    modulo = Modulo.query.get_or_404(id_modulo)
    
    # ids concluídos pelo usuário
    concluidas = {t.id_tarefa for t in TarefaUsuario.query.filter_by(id_usuario=current_user.id).all()}

    tarefas_json = []
    desbloqueada = True  # só a primeira não concluída fica desbloqueada

    for tarefa in tarefas:
        if tarefa.id_tarefa in concluidas:
            status = "concluida"
        elif desbloqueada:
            status = "desbloqueada"
            desbloqueada = False
        else:
            status = "bloqueada"
        tarefas_json.append({
            "id": tarefa.id_tarefa,
            "descicao": tarefa.descricao,
            "status": status
        })
            
    ofensiva = get_or_create_ofensiva(current_user.id)
    
    # Pega o horário atual em UTC, com timezone explícito
    agora = datetime.now().weekday()

    # Descobre o dia da semana (0 = segunda, 6 = domingo)
    dia_semana = agora

    return render_template(
        "modulo.html", 
        tarefas_json=tarefas_json, 
        id_modulo=id_modulo, 
        modulo=modulo,
        usuario=current_user,
        ranking=ranking,
        posicao_ranking=posicao_ranking,
        top5_bloco=top5_bloco,
        pontos = current_user.pontos,
        pontos_semanais=current_user.pontos_semanais,
        ofensiva=ofensiva,
        dia_semana=dia_semana,
        coins=current_user.moedas  # Ou current_user.coins, se esse for o nome
    )

@app.route("/introducao")
@login_required
def intro_page():
    if current_user.ja_passou_intro:
        return redirect(url_for("starting_page"))
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


    semana_atual = inicio_semana()

    bloco_usuario = (UsuarioBloco.query
        .join(Bloco)
        .filter(UsuarioBloco.id_usuario == current_user.id,
                Bloco.semana == semana_atual)
        .first())

    if not bloco_usuario:
        flash("Você ainda não está em um bloco esta semana.", "error")
        return redirect(url_for("dashboard"))

    ranking = (Usuario.query
        .join(UsuarioBloco)
        .filter(UsuarioBloco.id_bloco == bloco_usuario.id_bloco)
        .order_by(Usuario.pontos_semanais.desc())
        .all())
    
    
    # Busca o registro UsuarioBloco do usuário logado
    usuario_blocos = UsuarioBloco.query.filter_by(id_usuario=current_user.id).all()
    usuario_bloco = usuario_blocos[-1] if usuario_blocos else None

    if not usuario_bloco:
        top5_bloco = []  # Usuário não está em bloco
    else:
        id_bloco = usuario_bloco.id_bloco

    top5_bloco = (
        db.session.query(Usuario)
        .join(UsuarioBloco, Usuario.id == UsuarioBloco.id_usuario)
        .filter(UsuarioBloco.id_bloco == id_bloco)
        .order_by(desc(Usuario.pontos_semanais))
        .limit(5)
        .all()
    )
                
    ofensiva = get_or_create_ofensiva(current_user.id)
    
    # Pega o horário atual em UTC, com timezone explícito
    agora = datetime.now().weekday()

    # Descobre o dia da semana (0 = segunda, 6 = domingo)
    dia_semana = agora
    
    # Encontrar a posição do usuário no ranking
    posicao_ranking = next((i + 1 for i, u in enumerate(ranking) if u.id == current_user.id), None)

    return render_template(
        "quizes.html",
        usuario=current_user,
        usuarios=usuarios,
        ranking=ranking,
        posicao_ranking=posicao_ranking,
        top5_bloco=top5_bloco,
        pontos = current_user.pontos,
        pontos_semanais=current_user.pontos_semanais,
        ofensiva=ofensiva,
        dia_semana=dia_semana,
        coins=current_user.moedas  # Ou current_user.coins, se esse for o nome
    )

@app.route("/loja")
@login_required
def store_page():
    usuarios = Usuario.query.order_by(Usuario.pontos_semanais.desc()).all()
    
    poderes = Poderes.query.all()


    semana_atual = inicio_semana()

    bloco_usuario = (UsuarioBloco.query
        .join(Bloco)
        .filter(UsuarioBloco.id_usuario == current_user.id,
                Bloco.semana == semana_atual)
        .first())

    if not bloco_usuario:
        flash("Você ainda não está em um bloco esta semana.", "error")
        return redirect(url_for("dashboard"))

    ranking = (Usuario.query
        .join(UsuarioBloco)
        .filter(UsuarioBloco.id_bloco == bloco_usuario.id_bloco)
        .order_by(Usuario.pontos_semanais.desc())
        .all())
    
    # Busca o registro UsuarioBloco do usuário logado
    usuario_blocos = UsuarioBloco.query.filter_by(id_usuario=current_user.id).all()
    usuario_bloco = usuario_blocos[-1] if usuario_blocos else None

    if not usuario_bloco:
        top5_bloco = []  # Usuário não está em bloco
    else:
        id_bloco = usuario_bloco.id_bloco

    top5_bloco = (
        db.session.query(Usuario)
        .join(UsuarioBloco, Usuario.id == UsuarioBloco.id_usuario)
        .filter(UsuarioBloco.id_bloco == id_bloco)
        .order_by(desc(Usuario.pontos_semanais))
        .limit(5)
        .all()
    )
                    
    ofensiva = get_or_create_ofensiva(current_user.id)
    
    # Pega o horário atual em UTC, com timezone explícito
    agora = datetime.now().weekday()

    # Descobre o dia da semana (0 = segunda, 6 = domingo)
    dia_semana = agora
    
    # Encontrar a posição do usuário no ranking
    posicao_ranking = next((i + 1 for i, u in enumerate(ranking) if u.id == current_user.id), None)

    # Busca todos os poderes que o usuário possui
    poderes_usuario = PoderesUsuario.query.filter_by(id_usuario=current_user.id).all()

    # Cria um dicionário {id_poder: quantidade}
    quantidades = {pu.id_poder: pu.quantidade for pu in poderes_usuario}
    

    return render_template(
        "loja.html",
        usuario=current_user,
        poderes=poderes,
        top5_bloco=top5_bloco,
        usuarios=usuarios,
        posicao_ranking=posicao_ranking,
        ranking=ranking,
        pontos = current_user.pontos,
        pontos_semanais=current_user.pontos_semanais,
        quantidades=quantidades,
        ofensiva=ofensiva,
        dia_semana=dia_semana,
        coins=current_user.moedas  # Ou current_user.coins, se esse for o nome
    )

@app.route("/comprar_poder", methods=["POST"])
@login_required
def comprar_poder():
    id_poder = request.form.get("id_poder", type=int)

    if not id_poder:
        flash("ID do poder inválido.", "error")
        return redirect(url_for("store_page"))

    # Busca o poder no banco
    poder = db.session.get(Poderes, id_poder)
    if not poder:
        flash("Poder não encontrado.", "error")
        return redirect(url_for("store_page"))

    # Checa moedas do usuário
    if current_user.moedas < poder.preco:
        flash("Você não tem moedas suficientes!", "error")
        return redirect(url_for("store_page"))

    # Verifica se o usuário já tem esse poder
    poder_usuario = PoderesUsuario.query.filter_by(
        id_usuario=current_user.id,
        id_poder=poder.id_poder
    ).first()

    if poder_usuario:
        # Já existe → aumenta a quantidade
        poder_usuario.quantidade += 1
    else:
        # Não existe → cria novo registro com quantidade 1
        poder_usuario = PoderesUsuario(
            id_usuario=current_user.id,
            id_poder=poder.id_poder,
            quantidade=1
        )
        db.session.add(poder_usuario)

    # Desconta moedas
    current_user.moedas -= poder.preco

    # Salva tudo
    db.session.commit()

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
        semana_atual = inicio_semana()
        bloco_existente = (UsuarioBloco.query
            .join(Bloco)
            .filter(UsuarioBloco.id_usuario == current_user.id,
                    Bloco.semana == semana_atual)
            .first())

        if not bloco_existente:
            # Procura bloco com vaga
            bloco = (Bloco.query
                .filter(Bloco.semana == semana_atual)
                .join(UsuarioBloco)
                .group_by(Bloco.id_bloco)
                .having(db.func.count(UsuarioBloco.id_usuario) < 20)
                .first())

            if not bloco:
                # Cria novo bloco
                bloco = Bloco(semana=semana_atual)
                db.session.add(bloco)
                db.session.commit()

            # Adiciona usuário no bloco
            novo_registro = UsuarioBloco(
                id_usuario=current_user.id,
                id_bloco=bloco.id_bloco
            )
            db.session.add(novo_registro)
            db.session.commit()
        return jsonify({"mensagem": "Login efetuado com sucesso!"}), 200
    else:
        return jsonify({"mensagem": "Email/nome ou senha incorretos."}), 401
    
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

    desbloquear_conquista(current_user.id, "Eu sou eu mesmo")

    salvar_usuario(usuario)  # Atualiza o banco com os dados

    flash('Perfil atualizado com sucesso!')
    return redirect(url_for('perfil_page'))

def get_usuario_atual():
    return current_user

def get_or_create_ofensiva(id_usuario):
    ofensiva = Ofensiva.query.filter_by(id_usuario=id_usuario).first()
    diahoje = datetime.now()
    if not ofensiva:
        ofensiva = Ofensiva(
            id_usuario=current_user.id,
            dias_semana=[False]*7,
            recorde=0,
            sequencia_atual=0,
            data_ultima_atividade=diahoje
        )
        db.session.add(ofensiva)
        db.session.commit()
    return ofensiva

def desbloquear_conquista(id_usuario, conquista):
        # Se for string, buscar o ID pelo nome
    if isinstance(conquista, str):
        conquista_obj = Conquistas.query.filter_by(nome=conquista).first()
        if not conquista_obj:
            print(f"Conquista '{conquista}' não encontrada.")
            return
        id_conquista = conquista_obj.id_conquista
    else:
        id_conquista = conquista  # já é um número

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

def inicio_semana():
    hoje = date.today()
    # Ajustar para segunda-feira
    return hoje - timedelta(days=hoje.weekday())

@app.route("/concluir_tarefa/<int:id_tarefa>", methods=["POST"])
@login_required
def concluir_tarefa(id_tarefa):
    # buscar a tarefa
    tarefa = Tarefa.query.get_or_404(id_tarefa)

    # calcular pontuação (pode vir fixa da tarefa ou ser dinâmica)
    pontuacao = tarefa.pontuacao if hasattr(tarefa, "pontuacao") else 10  

    # verificar se já existe um registro para esse usuário e tarefa
    registro = TarefaUsuario.query.filter_by(
        id_usuario=current_user.id, id_tarefa=id_tarefa
    ).first()

    if registro:
        registro.concluida = True
        registro.pontuacao = pontuacao
    else:
        registro = TarefaUsuario(
            id_usuario=current_user.id,
            id_tarefa=id_tarefa,
            concluida=True,
            pontuacao=pontuacao
        )
        db.session.add(registro)

    current_user.pontos += tarefa.pontos
    current_user.pontos_semanais += tarefa.pontos

    ofensiva = get_or_create_ofensiva(current_user.id)
    if not ofensiva:
        return

    dia_semana = datetime.now().weekday()  # 0 = segunda, 6 = domingo

    ofensiva.dias_semana[dia_semana] = True
    db.session.commit()

    return jsonify({"message": "Tarefa concluída!", "pontuacao": pontuacao})

reset_codes = {}

@app.route("/esqueci_senha", methods=["GET", "POST"])
def esqueci_senha():
    if request.method == "POST":
        email = request.form.get("email")
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario:
            # Gera código aleatório
            codigo = ''.join(random.choices(string.digits, k=6))
            reset_codes[email] = codigo

            msg = Message(
                subject="Recuperação de Senha - Aurum",
                recipients=[email],
                body=f"Olá!\n\nSeu código de recuperação de senha é: {codigo}\n\nUse-o para redefinir sua senha no Aurum."
            )
            mail.send(msg)

            flash("Um código de verificação foi enviado para seu e-mail.")
            return redirect(url_for("resetar_senha", email=email))
        else:
            flash("E-mail não encontrado.")
    
    return render_template("esquecisenha.html")


@app.route("/resetar_senha/<email>", methods=["GET", "POST"])
def resetar_senha(email):
    if request.method == "POST":
        codigo = request.form.get("codigo")
        nova_senha = request.form.get("nova_senha")

        if reset_codes.get(email) == codigo:
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario:
                senha_hash = generate_password_hash(nova_senha)
                usuario.senha = senha_hash
                db.session.commit()

                reset_codes.pop(email)  # remove código usado
                flash("Senha alterada com sucesso. Faça login novamente.")
                return redirect(url_for("login_page"))
        else:
            flash("Código inválido ou expirado.")

    return render_template("redefinirsenha.html", email=email)

if __name__ == "__main__":
    #app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

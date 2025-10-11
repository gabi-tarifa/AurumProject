import ssl
import certifi
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

import math
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, Usuario, Modulo, Tarefa, Conquistas, UsuarioConquistas, Poderes
from models import Ofensiva, PoderesUsuario, Bloco, UsuarioBloco, TarefaUsuario, ConteudoTarefa, Configuracoes
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
from datetime import datetime, timedelta, date
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import desc
from flask_babel import Babel, _, format_datetime
from setup_modulos import criar_modulos
from setup_tarefas import criar_tarefas
from setup_conteudo import criar_conteudo
from flask_mail import Mail, Message
import random, string
import re
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail as sgMail

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass123@localhost:3306/Aurum' #Banco Local Tarifa
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL") #Banco Deploy
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
            
            dias_completos = sum(1 for dia in ofensiva.dias_semana if dia)

            if dias_completos == 7:
                user.moedas += 50
                print(f"Usuário {user.id} recebeu 50 moedas pela ofensiva semanal!")
            else:
                print(f"Usuário {user.id} não completou a ofensiva semanal.")

            # Resetar a contagem semanal sempre
            ofensiva.dias_semana = [False]*7

        db.session.commit()  # um único commit para todos

def checar_ofensivas():
    """
    Checa todas as ofensivas dos usuários na virada do dia.
    - Se já marcou atividade no dia atual -> não faz nada.
    - Se ontem teve atividade (dia_anterior=True) -> mantém sequência.
    - Se ontem não teve atividade -> zera sequência.
    - Atualiza dia_hoje/dia_anterior.
    """
    with app.app_context():
        hoje = date.today()
        ontem = hoje - timedelta(days=1)

        ofensivas = Ofensiva.query.all()

        for ofensiva in ofensivas:
            # Se já registrou atividade hoje, não mexe
            if ofensiva.data_ultima_atividade == hoje:
                # Move "dia_hoje" para "dia_anterior"
                ofensiva.dia_anterior = ofensiva.dia_hoje
                ofensiva.dia_hoje = False
                continue
            else:
                ofensiva.dia_anterior = ofensiva.dia_hoje
                ofensiva.dia_hoje = False
                ofensiva.sequencia_atual = 0


        db.session.commit()
    
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
    with app.app_context():
        recompensas = [70, 55, 45, 40, 40, 30, 30, 30, 30, 30,
                       20, 20, 20, 20, 20, 10, 10, 10, 10, 10]

        for i, usuario in enumerate(usuarios[:len(recompensas)]):
            usuario.moedas += recompensas[i]

           # Campeão (só o primeiro de cada bloco)
            if i == 0:
                usuario.vitorias += 1
                usuario.vitorias_consecutivas += 1
                desbloquear_conquista(usuario.id, "conquista_vencedor_nome")
                if usuario.vitorias >= 10:
                    desbloquear_conquista(usuario.id, "conquista_veterano_nome")
                if usuario.vitorias >= 100:
                    desbloquear_conquista(usuario.id, "conquista_campeao_nome")
                if usuario.vitorias_consecutivas >= 30:
                    desbloquear_conquista(usuario.id, "conquista_invicto_nome")
            else:
                usuario.vitorias_consecutivas = 0

def processar_premiacoes():
    with app.app_context():
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
scheduler.add_job(processar_premiacoes, 'cron', day_of_week='sun', hour=23, minute=59)
scheduler.add_job(checar_ofensivas, 'cron', hour=23, minute=59)
scheduler.start()

# 🔐 Página de Login
@app.route("/login")
def login_page():
    return render_template("login.html")

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Página do questionário de entrada
@app.route("/questionario")
@login_required
def questionario_page():
    return render_template("perguntasEntrada.html")

#Pagina de Configuracoes
@app.route("/config")
@login_required
def configuracoes():
    idiomas = [
        {"code": "pt", "name": "Português"},
        {"code": "en", "name": "English"}
    ]

    conf = Configuracoes.query.filter_by(id_usuario=current_user.id).first()
    if not conf:
        conf = Configuracoes(id_usuario=current_user.id, sons=True, musica=False)
        db.session.add(conf)
        db.session.commit()

    return render_template(
        "configuracoes.html",
        idiomas=idiomas,
        idioma=current_user.idioma,
        sons=conf.sons,
        musica=conf.musica,
        usuario=current_user
    )

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

@app.route("/modulo_<int:id_modulo>/tarefa_<int:numero_tarefa>")
@login_required
def licoes(numero_tarefa, id_modulo):
    tarefa = Tarefa.query.filter_by(id_modulo=id_modulo, numero_tarefa=numero_tarefa).first()
    blocos = []

    for c in tarefa.conteudos:
        if c.tipo == "texto":
            blocos.append({
                "tipo": "texto",
                # Traduz a chave armazenada no banco
                "conteudo": _(c.conteudo)
            })
        elif c.tipo == "quiz":
            alternativas = []
            if c.alternativas:
                opcoes = c.alternativas.split("||")
                for idx, opcao in enumerate(opcoes, start=1):
                    alternativas.append({
                        # Traduz cada chave de alternativa
                        "texto": _(opcao.strip()),
                        "correta": (idx == c.correta)
                    })
            blocos.append({
                "tipo": "quiz",
                # Traduz a pergunta
                "pergunta": _(c.pergunta),
                "alternativas": alternativas
            })

    return render_template(
        "licoes.html",
        tarefa=tarefa,
        blocos_json=blocos,
        numero_tarefa=tarefa.numero_tarefa
    )

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
        return redirect(url_for("login_page"))

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

    
    recompensas = [70, 55, 45, 40, 40, 30, 30, 30, 30, 30,
                   20, 20, 20, 20, 20, 10, 10, 10, 10, 10]
    
    ofen = Ofensiva.query.filter_by(id_usuario=current_user.id).first()
    
    dias_completos = sum(1 for dia in ofen.dias_semana if dia)
    semana_completa = dias_completos == 7


    return render_template(
        "ranking.html",
        usuario=current_user,
        usuarios=usuarios,
        posicao_ranking=posicao_ranking,
        pontos = current_user.pontos,
        pontos_semanais=current_user.pontos_semanais,
        ofensiva=ofensiva,
        dia_semana=dia_semana,
        recompensas=recompensas,
        ranking=ranking,
        semana_completa=semana_completa,
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
        return redirect(url_for("login_page"))

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
        
    ofensiva = get_or_create_ofensiva(current_user.id)

    ofen = Ofensiva.query.filter_by(id_usuario=current_user.id).first()
    
    dias_completos = sum(1 for dia in ofen.dias_semana if dia)
    semana_completa = dias_completos == 7

    # 🔹 Agora os módulos + progresso (com bloqueio sequencial)
    modulos = Modulo.query.order_by(Modulo.id).all()
    modulos_progresso = []

    for i, modulo in enumerate(modulos):
        # Total de tarefas do módulo
        tarefas = Tarefa.query.filter_by(id_modulo=modulo.id).all()
        tarefas_totais = len(tarefas)

        # Tarefas concluídas pelo usuário
        tarefas_feitas = (
            db.session.query(TarefaUsuario)
            .join(Tarefa, (TarefaUsuario.id_modulo == Tarefa.id_modulo) & (TarefaUsuario.numero_tarefa == Tarefa.numero_tarefa))
            .filter(
                TarefaUsuario.id_usuario == current_user.id,
                TarefaUsuario.id_modulo == modulo.id,
                TarefaUsuario.status == "concluida"
            )
            .count()
        )

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
        semana_completa=semana_completa,
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
        return redirect(url_for("login_page"))

    ranking = (Usuario.query
        .join(UsuarioBloco)
        .filter(UsuarioBloco.id_bloco == bloco_usuario.id_bloco)
        .order_by(Usuario.pontos_semanais.desc())
        .all())
    
    ofen = Ofensiva.query.filter_by(id_usuario=current_user.id).first()
    
    dias_completos = sum(1 for dia in ofen.dias_semana if dia)
    semana_completa = dias_completos == 7
    
    
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
        semana_completa=semana_completa,
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
        return redirect(url_for("login_page"))

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
    if ofensiva:
        ofen = Ofensiva.query.filter_by(id_usuario=current_user.id).first()

        dias_completos = sum(1 for dia in ofen.dias_semana if dia)
        semana_completa = dias_completos == 7

    # Encontrar a posição do usuário no ranking
    posicao_ranking = next((i + 1 for i, u in enumerate(ranking) if u.id == current_user.id), None)

    # todas as tarefas do módulo
    tarefas = Tarefa.query.filter_by(id_modulo=id_modulo).order_by(Tarefa.numero_tarefa).all()

    modulo = Modulo.query.get_or_404(id_modulo)

    # ids concluídos pelo usuário
    concluidas = {t.numero_tarefa for t in TarefaUsuario.query.filter_by(id_usuario=current_user.id).all()}

    tarefas_json = []
    desbloqueada = True  # só a primeira não concluída fica desbloqueada

    for tarefa in tarefas:
        if tarefa.numero_tarefa in concluidas:
            status = "concluida"
        elif desbloqueada:
            status = "desbloqueada"
            desbloqueada = False
        else:
            status = "bloqueada"
        tarefas_json.append({
            "numero_tarefa": tarefa.numero_tarefa,
            "descicao": tarefa.descricao,
            "status": status
        })


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
        semana_completa=semana_completa,
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
        return redirect(url_for("login_page"))

    ranking = (Usuario.query
        .join(UsuarioBloco)
        .filter(UsuarioBloco.id_bloco == bloco_usuario.id_bloco)
        .order_by(Usuario.pontos_semanais.desc())
        .all())
    
    ofen = Ofensiva.query.filter_by(id_usuario=current_user.id).first()
    
    dias_completos = sum(1 for dia in ofen.dias_semana if dia)
    semana_completa = dias_completos == 7
    
    
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
        semana_completa=semana_completa,
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
        return redirect(url_for("login_page"))

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

    ofen = Ofensiva.query.filter_by(id_usuario=current_user.id).first()
    
    dias_completos = sum(1 for dia in ofen.dias_semana if dia)
    semana_completa = dias_completos == 7
                    
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
        semana_completa=semana_completa,
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

@app.route("/api/config/apelido", methods=["POST"])
@login_required
def alterar_apelido():
    data = request.get_json()
    novo_apelido = data.get("apelido")
    current_user.nome = novo_apelido
    db.session.commit()
    return jsonify({"message": "Apelido atualizado com sucesso!"})


@app.route("/api/config/email", methods=["POST"])
@login_required
def alterar_email():
    data = request.get_json()
    novo_email = data.get("email")
    current_user.email = novo_email
    db.session.commit()
    return jsonify({"message": "Email atualizado com sucesso!"})


@app.route("/api/config/senha", methods=["POST"])
@login_required
def alterar_senha():
    data = request.get_json()
    senha_atual = data.get("atual")
    nova_senha = data.get("nova")

    if not check_password_hash(current_user.senha, senha_atual):
        return jsonify({"message": "Senha atual incorreta!"}), 400

    current_user.senha = generate_password_hash(nova_senha)
    db.session.commit()
    return jsonify({"message": "Senha alterada com sucesso!"})

@app.route("/api/config/reset", methods=["POST"])
@login_required
def resetar_config():
    # buscar as configurações do usuário
    conf = Configuracoes.query.filter_by(id_usuario=current_user.id).first()

    if not conf:
        # se não existir, cria com valores padrão
        conf = Configuracoes(id_usuario=current_user.id, sons=True, musica=False)
        db.session.add(conf)
    else:
        # resetar para padrão
        conf.sons = True
        conf.musica = False

    db.session.commit()
    return jsonify({"message": "Configurações redefinidas com sucesso!", 
                    "sons": conf.sons, "musica": conf.musica})

@app.route("/api/config", methods=["POST"])
@login_required
def salvar_config():
    data = request.get_json()

    conf = Configuracoes.query.filter_by(id_usuario=current_user.id).first()
    if not conf:
        conf = Configuracoes(id_usuario=current_user.id)
        db.session.add(conf)

    if "sons" in data:
        conf.sons = bool(data["sons"])
    if "musica" in data:
        conf.musica = bool(data["musica"])

    db.session.commit()
    return jsonify({"success": True})

@app.route("/api/config", methods=["GET"])
@login_required
def get_config():
    conf = Configuracoes.query.filter_by(id_usuario=current_user.id).first()
    if not conf:
        conf = Configuracoes(id_usuario=current_user.id)
        db.session.add(conf)
        db.session.commit()

    return jsonify({
        "sons": conf.sons,
        "musica": conf.musica
    })

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

        if current_user.is_authenticated:
            conf = Configuracoes.query.filter_by(id_usuario=current_user.id).first()
            if not conf:
                conf = Configuracoes(id_usuario=current_user.id)
                db.session.add(conf)
                db.session.commit()

        semana_atual = inicio_semana()
        if not usuario.entrada:
            usuario.entrada = datetime.now()
            db.session.commit()
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
    conquistas_a_dar = ["conquista_og_nome"]
    
    for nome in conquistas_a_dar:
        conquista = Conquistas.query.filter_by(nome=nome).first()
        if conquista:
            desbloquear_conquista(current_user.id, conquista.id_conquista)

    return redirect(url_for("perfil_page"))
    
@app.route("/ifsp413")
@login_required
def ifiano413():
    conquistas_a_dar = ["conquista_farinha_nome"]
    
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

    desbloquear_conquista(current_user.id, "conquista_customizou_perfil_nome")

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
            data_ultima_atividade=diahoje,
            dia_hoje=False,
            dia_anterior=False
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

@app.route("/concluir_tarefa/modulo_<int:id_modulo>/tarefa_<int:numero_tarefa>", methods=["POST"])
@login_required
def concluir_tarefa(id_modulo, numero_tarefa):
    # buscar a tarefa com chave composta
    tarefa = Tarefa.query.filter_by(
        id_modulo=id_modulo,
        numero_tarefa=numero_tarefa
    ).first_or_404()

    # pontuação base da tarefa
    pontuacao_base = tarefa.pontos if hasattr(tarefa, "pontos") else 10  

    # verificar se já existe um registro para esse usuário e tarefa
    registro = TarefaUsuario.query.filter_by(   
        id_usuario=current_user.id,
        id_modulo=id_modulo,
        numero_tarefa=numero_tarefa
    ).first()

    if registro:
        # já existe → incrementar repetição
        registro.repeticao += 1
        registro.status = "concluida"

        # aplicar lógica do desconto
        descontador = min(math.ceil(registro.repeticao / 2), 5)
        registro.pontuacao = pontuacao_base // descontador
    else:
        # primeira vez concluindo
        registro = TarefaUsuario(
            id_usuario=current_user.id,
            id_modulo=id_modulo,
            numero_tarefa=numero_tarefa,
            status="concluida",
            pontuacao=pontuacao_base,
            repeticao=1
        )
        db.session.add(registro)

    # atualizar pontos do usuário com a pontuação já descontada
    current_user.pontos += registro.pontuacao
    current_user.pontos_semanais += registro.pontuacao
    current_user.moedas += registro.pontuacao/2 

    if current_user.pontos >= 100:
        desbloquear_conquista(current_user.id, "conquista_em_crescimento_nome")
    if current_user.pontos >= 1000:
        desbloquear_conquista(current_user.id, "conquista_experiente_nome")
    if current_user.pontos >= 10000:
        desbloquear_conquista(current_user.id, "conquista_guru_nome")
    if current_user.pontos >= 999999:
        desbloquear_conquista(current_user.id, "conquista_aurum_master_nome")

    # manter lógica da ofensiva
    ofensiva = get_or_create_ofensiva(current_user.id)
    if ofensiva:
        dia_semana = datetime.now().weekday()  # 0 = segunda, 6 = domingo

        if not ofensiva.dia_hoje:
            ofensiva.data_ultima_atividade = datetime.now()
            ofensiva.sequencia_atual = 1
            if ofensiva.sequencia_atual > ofensiva.recorde:
                ofensiva.recorde = ofensiva.s


    
    if ofensiva.sequencia_atual >= 1 or ofensiva.recorde >= 1:
        desbloquear_conquista(current_user.id, "conquista_primeira_ofensiva_nome")
    if ofensiva.sequencia_atual >= 7 or ofensiva.recorde >= 7:
        desbloquear_conquista(current_user.id, "conquista_semana_fogo_nome")
    if ofensiva.sequencia_atual >= 30 or ofensiva.recorde >= 30:
        desbloquear_conquista(current_user.id, "conquista_persistente_nome")
    if ofensiva.sequencia_atual >= 180 or ofensiva.recorde >= 180:
        desbloquear_conquista(current_user.id, "conquista_imparavel_nome")
    if ofensiva.sequencia_atual >= 365 or ofensiva.recorde >= 365:
        desbloquear_conquista(current_user.id, "conquista_lenda_constancia_nome")


    ofensiva.dias_semana[dia_semana] = True
    ofensiva.dia_hoje = True
    db.session.commit()

    return jsonify({
        "message": "Tarefa concluída!",
        "pontuacao": registro.pontuacao,
        "repeticao": registro.repeticao
        })

@app.route("/licao_falha/<int:numero_tarefa>/<int:id_modulo>")
@login_required
def licao_falha(numero_tarefa, id_modulo):
    # Busca tarefa só pra exibir nome/título se quiser
    tarefa = Tarefa.query.filter_by(
        id_modulo=id_modulo,
        numero_tarefa=numero_tarefa
    ).first_or_404()

    return render_template("falha.html", tarefa=tarefa, id_modulo=id_modulo)

@app.route("/licao_sucesso/<int:numero_tarefa>/<int:id_modulo>")
@login_required
def licao_sucesso(numero_tarefa, id_modulo):
    tarefa = Tarefa.query.filter_by(
        id_modulo=id_modulo,
        numero_tarefa=numero_tarefa
    ).first_or_404()

    return render_template("sucesso.html", tarefa=tarefa, id_modulo=id_modulo)

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

            corpo = f"Olá {usuario.nome}!<br><br>Seu código de recuperação de senha é: {codigo}<br><br>Use-o para redefinir sua senha no Aurum."
            send_email_via_api(email, "Recuperação de Senha - Aurum", corpo)

            flash("Um código de verificação foi enviado para seu e-mail.")
            return redirect(url_for("resetar_senha", email=email))
        else:
            flash("E-mail não encontrado.")
    
    return render_template("esquecisenha.html")



def senha_valida(senha: str) -> bool:
    if len(senha) < 6 or len(senha) > 16:
        return False
    if not re.search(r"[A-Z]", senha):  # pelo menos 1 maiúscula
        return False
    if not re.search(r"[a-z]", senha):  # pelo menos 1 minúscula
        return False
    if not re.search(r"\d", senha):     # pelo menos 1 número
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):  # especial
        return False
    return True


@app.route("/resetar_senha/<email>", methods=["GET", "POST"])
def resetar_senha(email):
    if request.method == "POST":
        codigo = request.form.get("codigo")
        nova_senha = request.form.get("nova_senha")
        confirmar_senha = request.form.get("confirmar_senha")

        if reset_codes.get(email) == codigo:
            if nova_senha != confirmar_senha:
                flash("As senhas não coincidem.")
                return redirect(request.url)

            if not senha_valida(nova_senha):
                flash("A senha não atende aos requisitos de segurança.")
                return redirect(request.url)

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

@app.route('/suporte', methods=['GET', 'POST'])
@login_required
def enviar_ticket():
    if request.method == 'POST':
        nome = request.form['nome']
        email_usuario = request.form['email']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']

        # gerar um ID de oito digitos para o ticket
        ticket_id = random.randint(10000000, 99999999)
        
        titulo_suporte = f"[SUPORTE] Ticket {ticket_id} - {assunto}"

        email_suporte = "grupomoneto2025@gmail.com"

        # email para o suporte
        # suporte
        corpo_suporte = f"""
            Novo ticket recebido:<br><br>

            ID do Ticket: {ticket_id}<br>
            Nome: {nome}<br>
            Email: {email_usuario}<br>
            Assunto: {assunto}<br>
            Mensagem:<br>
            {mensagem}
        """
        send_email_via_api(email_suporte, titulo_suporte, corpo_suporte)

        titulo_suporte_usuario = f"[Aurum] Recebemos seu ticket #{ticket_id}"

        corpo_usuario = f"""
            Olá {nome},<br><br>

            Recebemos sua solicitação de suporte. Nosso time entrará em contato em breve.<br><br>

            ID do seu ticket: {ticket_id}<br>
            Assunto: {assunto}<br><br>

            Descrição:<br>
            {mensagem}
            <br><br>
            Obrigado por nos contatar,<br>
            Equipe Aurum
            """
        send_email_via_api(email_usuario, titulo_suporte, corpo_usuario)

        flash("Seu ticket foi enviado com sucesso! Verifique seu email.", "success")
        return redirect(url_for("starting_page"))

    return render_template("enviarticket.html")

def send_email_via_api(destinatario, assunto, conteudo):
    # Garante que o destinatário seja string e não tupla
    if isinstance(destinatario, (tuple, list)):
        destinatario = destinatario[0]  # pega só o e-mail, se vier em tupla

    message = sgMail(
        from_email='grupomoneto2025@gmail.com',
        to_emails=destinatario,  # aqui deve ser string tipo "exemplo@gmail.com"
        subject=assunto,
        html_content=conteudo
    )

    print(os.environ.get('SENDGRID_API_KEY'))

    if os.environ.get('SENDGRID_API_KEY') == None:
        sucesso = send_email_flask_mail(destinatario, assunto, conteudo)
        print(sucesso)
        if sucesso:
            return

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"[SendGrid] Status: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return "ERRO"
    
def send_email_flask_mail(destinatario, assunto, conteudo)->bool:
    message = Message(
        subject=assunto,
        sender=("Aurum Suporte", "grupomoneto2025@gmail.com"),
        recipients=[destinatario],
        body=conteudo
    )
    try:
        mail.send(message)
        return True
    except Exception as e:
        print(f"Erro ao enviar o email via Flask Mail: {e}")
        return False

if __name__ == "__main__":
    app.run(debug=True)
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host="0.0.0.0", port=port)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from flask_login import UserMixin
from sqlalchemy.ext.mutable import MutableList

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'Usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    pontos = db.Column(db.Integer, default=0, nullable=False)
    pontos_semanais = db.Column(db.Integer, default=0, nullable=False)
    moedas = db.Column(db.Integer, default = 0, nullable= False)
    profilepicture = db.Column(db.String(255), nullable=False, default="img/user.png")
    backgroundpicture = db.Column(db.String(255), nullable=False, default="img/rectangle.png")
    ja_passou_intro = db.Column(db.Boolean, default=False)
    idioma = db.Column(db.String(20), nullable=False, default="pt")
    entrada = db.Column(db.Date)
    vitorias = db.Column(db.Integer, nullable=False, default=0)
    vitorias_consecutivas = db.Column(db.Integer, nullable=False, default=0)
    moduloinicial = db.Column(db.Integer, nullable=False, default=1)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "pontos": self.pontos,
            "pontos_semanais": self.pontos_semanais,
            "moedas": self.moedas,
            "profilepicture": self.profilepicture,
            "backgroundpicture": self.backgroundpicture,
            "ja_passou_intro": self.ja_passou_intro,
            "idioma": self.idioma,
            "entrada": self.entrada,
            "vitorias": self.vitorias,
            "vitorias_consecutivas": self.vitorias_consecutivas,
            "moduloinicial": self.moduloinicial
        }


    def __repr__(self):
        return f'<Usuario {self.nome} - {self.email}>'

class Modulo(db.Model):
    __tablename__ = 'Modulo'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao
        }

class Tarefa(db.Model):
    __tablename__ = 'Tarefa'

    pontos = db.Column(db.Integer, nullable=False)    
    id_modulo = db.Column(db.Integer,  ForeignKey("Modulo.id"), primary_key=True)
    numero_tarefa = db.Column(db.Integer, primary_key=True)

    descricao = db.Column(db.String(255), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('id_modulo', 'numero_tarefa'),
    )

    # 🔹 RELAÇÃO COM ConteudoTarefa
    conteudos = db.relationship(
        "ConteudoTarefa",
        backref="tarefa",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {

            "id_modulo": self.id_modulo,
            "numero_tarefa": self.numero_tarefa,
            "descricao": self.descricao,
            "pontos": self.pontos,
            "conteudos": [c.to_dict() for c in self.conteudos]
        }

class ConteudoTarefa(db.Model):
    __tablename__ = 'ConteudoTarefa'

    id_conteudo = db.Column(db.Integer, primary_key=True)

    numero_tarefa = db.Column(db.Integer, nullable=False)
    id_modulo = db.Column(db.Integer, nullable=False)

    tipo = db.Column(db.String(15))
    conteudo = db.Column(db.Text)
    pergunta = db.Column(db.Text)
    alternativas = db.Column(db.Text)
    correta = db.Column(db.Integer)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['id_modulo', 'numero_tarefa'],
            ['Tarefa.id_modulo', 'Tarefa.numero_tarefa']
        ),
    )

    def to_dict(self):
        return {
            "id_conteudo": self.id_conteudo,
            "numero_tarefa": self.numero_tarefa,
            "id_modulo": self.id_modulo,
            "tipo": self.tipo,
            "conteudo": self.conteudo,
            "pergunta": self.pergunta,
            "alternativas": self.alternativas.split("||") if self.alternativas else [],
            "correta": self.correta
        }


class TarefaUsuario(db.Model):
    __tablename__ = 'TarefaUsuario'

    id_tarefa_usuario = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, ForeignKey("Usuario.id"), nullable=False)

    id_modulo = db.Column(db.Integer, ForeignKey("Modulo.id"))
    numero_tarefa = db.Column(db.Integer)
    pontuacao = db.Column(db.Integer, nullable=False, default=0)
    repeticao = db.Column(db.Integer, nullable=False, default=0)

    status = db.Column(db.String(20), default="pendente")

    __table_args__ = (
        ForeignKeyConstraint(
            ['id_modulo', 'numero_tarefa'],
            ['Tarefa.id_modulo', 'Tarefa.numero_tarefa']
        ),
    )

    def to_dict(self):
        return {
            "id_tarefa_usuario": self.id_tarefa_usuario,
            "id_tarefa": self.id_tarefa,
            "id_usuario": self.id_usuario,
            "data_conclusao": self.data_conclusao.isoformat() if self.data_conclusao else None,
            "pontuacao": self.pontuacao,
            "repeticao": self.repeticao
        }


class Conquistas(db.Model):
    __tablename__ = 'Conquistas'

    id_conquista = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    imagem = db.Column(db.String(255), nullable=False, default="img/gold-medal.png")
    cor = db.Column(db.String(10), nullable=False, default="azul")
    raridade = db.Column(db.String(10), nullable=False, default="regular")

    def to_dict(self):
        return {
            "id_conquista": self.id_conquista,
            "nome": self.nome,
            "descricao": self.descricao,
            "imagem": self.imagem,
            "cor": self.cor,
            "raridade": self.raridade
        }


class UsuarioConquistas(db.Model):
    __tablename__ = 'UsuarioConquistas'

    id_usuario_conquista = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, ForeignKey(Usuario.id), nullable=False)
    id_conquista = db.Column(db.Integer, ForeignKey(Conquistas.id_conquista), nullable=False)

    def to_dict(self):
        return {
            "id_usuario_conquista": self.id_usuario_conquista,
            "id_usuario": self.id_usuario,
            "id_conquista": self.id_conquista
        }

class Poderes(db.Model):
    __tablename__ = "Poderes"

    id_poder = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Integer, nullable=False)  
    imagem = db.Column(db.String(255), default="", nullable=False)  # Caminho para o ícone

    def __repr__(self):
        return f"<Poder {self.nome}>"

    def to_dict(self):
        return {
            "id_poder": self.id_poder,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "imagem": self.imagem
        }

class PoderesUsuario(db.Model):
    __tablename__ = "PoderesUsuario"

    id_poder_usuario = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, ForeignKey(Usuario.id), nullable=False)
    id_poder = db.Column(db.Integer, ForeignKey(Poderes.id_poder), nullable=False)
    quantidade = db.Column(db.Integer, default=1)  # Ex.: se o poder for acumulável

    def __repr__(self):
        return f"<PoderesUsuario usuario={self.id_usuario} poder={self.id_poder}>"

    def to_dict(self):
        return {
            "id_poder_usuario": self.id_poder_usuario,
            "id_usuario": self.id_usuario,
            "id_poder": self.id_poder,
            "quantidade": self.quantidade
        }

class Bloco(db.Model):
    __tablename__ = "Bloco"

    id_bloco = db.Column(db.Integer, primary_key=True)
    semana = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            "id_bloco": self.id_bloco,
            "semana": self.semana.isoformat() if self.semana else None
        }

class UsuarioBloco(db.Model):
    __tablename__ = "UsuarioBloco"

    id_usuario_bloco = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, ForeignKey(Usuario.id), nullable=False)
    id_bloco = db.Column(db.Integer,  ForeignKey(Bloco.id_bloco), nullable=False)

    def to_dict(self):
        return {
            "id_usuario_bloco": self.id_usuario_bloco,
            "id_usuario": self.id_usuario,
            "id_bloco": self.id_bloco
}

class Ofensiva(db.Model):
    __tablename__ = "Ofensiva"

    id_ofensiva = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer,  ForeignKey(Usuario.id), nullable=False)

    # Última vez que o usuário registrou atividade
    data_ultima_atividade = db.Column(db.Date)

    # Dias consecutivos atuais (ofensiva em andamento)
    sequencia_atual = db.Column(db.Integer, default=0)

    # Maior sequência já atingida
    recorde = db.Column(db.Integer, default=0)

    dias_semana = db.Column(MutableList.as_mutable(db.JSON),default=lambda: [False]*7,nullable=False)

    dia_hoje = db.Column(db.Boolean, default=False)
    dia_anterior = db.Column(db.Boolean, default=False)

class Configuracoes(db.Model):
    __tablename__ = "configuracoes"

    id_config = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, ForeignKey(Usuario.id), nullable=False)

    sons = db.Column(db.Boolean, default=True)
    musica = db.Column(db.Boolean, default=True)

    tema = db.Column(db.String(6), nullable=False, default="esc")

    musica_tocada = db.Column(db.Text, nullable=False, default="/static/sounds/music/taswell.mp3")

    volume_musica = db.Column(db.Integer, nullable=False, default=70)

class Amizade(db.Model):
    __tablename__ = "Amizade"

    id_usuario1 = db.Column(db.Integer, db.ForeignKey("Usuario.id"), primary_key=True, nullable=False)
    id_usuario2 = db.Column(db.Integer, db.ForeignKey("Usuario.id"), primary_key=True, nullable=False)
    status = db.Column(db.String(20), default="pendente")
    data_criacao = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (
        db.CheckConstraint('id_usuario1 <> id_usuario2', name='chk_diferentes'),
        db.CheckConstraint('id_usuario1 < id_usuario2', name='chk_ordem'),  # evita duplicações invertidas
    )

    usuario1 = db.relationship("Usuario", foreign_keys=[id_usuario1], backref="amizades_enviadas")
    usuario2 = db.relationship("Usuario", foreign_keys=[id_usuario2], backref="amizades_recebidas")

    def to_dict(self):
        return {
            "id_usuario1": self.id_usuario1,
            "id_usuario2": self.id_usuario2,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None
        }

    def __repr__(self):
        return f"<Amizade {self.id_usuario1} ↔ {self.id_usuario2}>"

class MusicasUsuario(db.Model):
    __tablename__ = "MusicasUsuario"

    id_musicas_usuario = db.Column(db.Integer, primary_key=True, nullable=False)
    id_usuario = db.Column(db.Integer, ForeignKey(Usuario.id), nullable=False )
    nome_musica = db.Column(db.String(25), nullable=False)
    caminho = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id_musicas_usuario,
            "id_usuario": self.id_usuario,
            "nome": self.nome_musica,
            "caminho": self.caminho
        }
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'Usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    pontos = db.Column(db.Integer, default=0, nullable=False)
    profilepicture = db.Column(db.String(255), nullable=False, default="img/user.png")
    backgroundpicture = db.Column(db.String(255), nullable=False, default="img/rectangle.png")

    def __repr__(self):
        return f'<Usuario {self.nome} - {self.email}>'

class Modulo(db.Model):
    __tablename__ = 'Modulo'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)

class Tarefa(db.Model):
    __tablename__ = 'Tarefa'

    id_tarefa = db.Column(db.Integer, primary_key=True)
    id_modulo = db.Column(db.Integer, ForeignKey(Modulo.id), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    pontos = db.Column(db.Integer, nullable=False)

class TarefaUsuario(db.Model):
    __tablename__ = 'TarefaUsuario'

    id_tarefa_usuario = db.Column(db.Integer, primary_key=True)
    id_tarefa = db.Column(db.Integer, ForeignKey(Tarefa.id_tarefa),nullable=False)
    id_modulo = db.Column(db.Integer, ForeignKey(Modulo.id), nullable=False)
    data_conclusao = db.Column(db.Date, nullable=False)
    pontuacao = db.Column(db.Integer, nullable=False)

class Conquistas(db.Model):
    __tablename__ = 'Conquistas'

    id_conquista = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    imagem = db.Column(db.String(255), nullable=False, default="https://cdn-icons-png.flaticon.com/128/5355/5355671.png")
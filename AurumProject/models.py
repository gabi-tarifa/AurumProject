from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'Usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome} - {self.email}>'

class Modulo(db.model):
    __tablename__ = 'Modulo'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)

class Tarefa(db.model):
    __tablename__ = 'Tarefa'

    id_tarefa = db.Column(db.Integer, primary_key=True)
    id_modulo = db.Column(db.Integer, ForeignKey(Modulo.id), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    pontos = db.Column(db.Integer, nullabe=False)


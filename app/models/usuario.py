from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint
import uuid
from sqlalchemy.sql import func

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    data_cadastro = db.Column(db.TIMESTAMP, server_default=func.now())

    def __init__(self, nome, email, senha):
        self._nome = nome
        self._email = email
        self._senha = senha

    def __repr__(self) -> str:
        return f'<Usuario: {self._nome}, Email: {self._email}, Senha: {self._senha}>'






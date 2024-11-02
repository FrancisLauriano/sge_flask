from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    pedidos = relationship('Pedido', back_populates='cliente', cascade='all, delete-orphan')

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

    def __repr__(self) -> str:
        return f'<Nome: {self.nome}, Email: {self.email}>'
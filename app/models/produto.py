from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import uuid

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    id_categoria = db.Column(UUID(as_uuid=True), ForeignKey('categorias.id', ondelete='SET NULL'))

    categoria = relationship('Categoria', back_populates='produtos')
    detalhe_pedido = relationship('DetalhePedido', back_populates='produto', cascade="all, delete-orphan")

    def __init__(self, nome, id_categoria):
        self.nome = nome
        self.id_categoria = id_categoria 
        
    def __repr__(self) -> str:
        return f'<Nome: {self.nome}, id_categoria: {self.id_categoria}>'
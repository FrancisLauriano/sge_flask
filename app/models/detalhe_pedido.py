from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import uuid

class DetalhePedido(db.Model):
    __tablename__ = 'detalhe_pedidos'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_pedido = db.Column(UUID(as_uuid=True), ForeignKey('pedidos.id', ondelete='CASCADE'), nullable=False)
    id_produto = db.Column(UUID(as_uuid=True), ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    desconto = db.Column(db.Numeric(10, 2), nullable=False)

    pedido = relationship('Pedido', back_populates='detalhe_pedidos')

    produto = relationship('Produto', back_populates='detalhe_pedidos')

    def __init__(self, id_pedido, id_produto, valor, desconto):
        self._id_pedido = id_pedido
        self._id_produto = id_produto 
        self._valor = valor
        self._desconto = desconto
        
    def __repr__(self) -> str:
        return f'<ID Pedido: {self.id_pedido}, ID Produto: {self._id_produto}, Valor: {self._valor}, Desconto: {self._desconto} >'




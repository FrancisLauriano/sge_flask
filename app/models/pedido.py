from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.sql import func
import uuid

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_compra = db.Column(db.TIMESTAMP, server_default=func.now())
    cliente_id = db.Column(UUID(as_uuid=True), ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False)

    cliente = relationship('Cliente', back_populates='pedidos')

    detalhe_pedido = relationship('DetalhePedido', back_populates='detalhe_pedido', cascade="all, delete-orphan")

    def __init__(self, data_compra, cliente_id):
        self._data_compra = data_compra
        self._cliente_id = cliente_id

    def __repr__(self) -> str:
        return f'<Data compra: {self._data_compra}, Cliente ID: {self._cliente_id}>'

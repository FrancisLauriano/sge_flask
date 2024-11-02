from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)

    produtos = relationship('Produto', back_populates='categoria')

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self) -> str:
        return f'Nome: {self.nome}'
from app import db
from app.models.produto import Produto
from flask import request, jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, validate, ValidationError

produto = Blueprint('produtos', __name__)

class ProdutoSchema(Schema):
    nome = fields.String(required=True, validate=validate.Length(min=3, max=255))
    id_categoria = fields.String(required=True)
    

@produto.route('/produtos', methods=['POST'])
@jwt_required()
def create_produto():
    data = request.get_json()
    schema = ProdutoSchema() 

    try:
        valida_data = schema.load(data)

        nome = valida_data.get('nome').lower()
        id_categoria = valida_data.get('id_categoria').lower()

        if not nome or not id_categoria:
            abort(400, description="Nome e categoria são campos obrigatórios.")

        novo_produto = Produto(nome=nome, id_categoria=id_categoria)

        db.session.add(novo_produto)
        db.session.commit()

        return jsonify(
            {
                'id': novo_produto.id,
                'nome': novo_produto.nome,
                'id_categoria': novo_produto.id_categoria
            }
        ), 201
    
    except ValidationError as ve:
        abort(400, description=f"Erro na validação dos dados: {ve.messages}")

    except Exception as e:
        abort(500, description=f"Erro no cadastro do produto: {str(e)}")


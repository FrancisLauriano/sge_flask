from app import db
from app.models.produto import Produto
from flask import request, jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, validate, ValidationError
from sqlalchemy.orm import joinedload

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
        id_categoria = valida_data.get('id_categoria')

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


@produto.route('/produtos/<string:id>', methods=['PUT'])
@jwt_required()
def update_produto(id):
    data = request.get_json()
    schema = ProdutoSchema()

    produto = Produto.query.get(id)

    if not produto:
        abort(404, description="Produto não encontrado.")
    
    try:
        valida_data = schema.load(data)

        nome = valida_data.get('nome').lower()
        id_categoria = valida_data.get('id_categoria')

        produto.nome = nome
        produto.id_categoria = id_categoria

        db.session.commit()

        return jsonify(
            {
                'id': produto.id,
                'nome': produto.nome,
                'id_categoria': produto.id_categoria,
            }
        ), 200
    
    except ValidationError as ve:
        abort(400, description=f"Erro na validação dos dados: {ve.messages}")

    except Exception as e:
        abort(500, description=f"Erro ao atualizar o produto: {str(e)}")


@produto.route('/produtos', methods=['GET'])
@jwt_required()
def get_all_produto():
    try:
        produtos = Produto.query.options(joinedload(Produto.categoria)).all()

        if not produtos:
            abort(404, description="Nenhum produto encontrado.")

        return jsonify([
            {
                'id': produto.id,
                'nome': produto.nome,
                'id_categoria': produto.id_categoria,
                'nome_categoria': produto.categoria.nome if produto.categoria else None
            } for produto in produtos
        ]), 200
    
    except Exception as e:
        abort(500, description=f"Erro ao listar produtos: {str(e)}")        


@produto.route('/produtos/<string:id>', methods=['GET'])
@jwt_required()
def get_by_id_produto(id):
    try:
        produto = Produto.query.filter_by(id=id).options(joinedload(Produto.categoria)).first()

        if not produto:
            abort(404, description="Produto não encontrado.")

        return jsonify(
            {
                'id': produto.id,
                'nome': produto.nome,
                'id_categoria': produto.id_categoria,
                'nome_categoria': produto.categoria.nome if produto.categoria else None
            }
        ), 200
    
    except Exception as e:
        abort(500, description=f"Erro ao buscar produto: {str(e)}")                


@produto.route('/produtos/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_by_id_produto(id):
    try:
        produto = Produto.query.get(id)

        if not produto:
            abort(404, description="Produto não encontrado.")

        db.session.delete(produto)
        db.session.commit()
        
        return '', 204
    
    except Exception as e:
        abort(500, description=f"Erro ao excluir produto: {str(e)}")

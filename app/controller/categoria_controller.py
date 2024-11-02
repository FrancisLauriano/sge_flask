from app import db
from app.models.categoria import Categoria
from flask import request, jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, validate, ValidationError
from sqlalchemy.orm import joinedload

categoria = Blueprint('categorias', __name__)

class CategoriaSchema(Schema):
    nome = fields.String(required=True, validate=validate.Length(min=3, max=255))


@categoria.route('/categorias', methods=['POST'])
@jwt_required()
def create_categoria():
    data = request.get_json()
    schema = CategoriaSchema() 

    try:
        valida_data = schema.load(data)

        nome = valida_data.get('nome').lower()

        nova_categoria = Categoria(nome=nome)

        db.session.add(nova_categoria)
        db.session.commit()

        return jsonify(
            {
                'id': nova_categoria.id,
                'nome': nova_categoria.nome
            }
        ), 201
    
    except ValidationError as ve:
        abort(400, description=f"Erro na validação dos dados: {ve.messages}")

    except Exception as e:
        abort(500, description=f"Erro no cadastro da categoria: {str(e)}")


@categoria.route('/categorias/<string:id>', methods=['PUT'])
@jwt_required()
def update_categoria(id):
    data = request.get_json()
    schema = CategoriaSchema()

    categoria = Categoria.query.get(id)

    if not categoria:
        abort(404, description="Categoria não encontrada.")
    
    try:
        valida_data = schema.load(data)

        nome = valida_data.get('nome').lower()

        categoria.nome = nome

        db.session.commit()

        return jsonify(
            {
                'id': categoria.id,
                'nome': categoria.nome
            }
        ), 200
    
    except ValidationError as ve:
        abort(400, description=f"Erro na validação dos dados: {ve.messages}")

    except Exception as e:
        abort(500, description=f"Erro ao atualizar a categoria: {str(e)}")


@categoria.route('/categorias', methods=['GET'])
@jwt_required()
def get_all_categoria():
    try:
        categorias = Categoria.query.all()

        if not categorias:
            abort(404, description="Nenhuma categoria encontrada.")

        return jsonify([
            {
                'id': categoria.id,
                'nome': categoria.nome
            } for categoria in categorias
        ]), 200
    
    except Exception as e:
        abort(500, description=f"Erro ao listar categorias: {str(e)}")        


@categoria.route('/categorias/<string:id>', methods=['GET'])
@jwt_required()
def get_by_id_categoria(id):
    try:
        categoria = Categoria.query.filter_by(id=id).options(joinedload(Categoria.produtos)).first()

        if not categoria:
            abort(404, description="Categoria não encontrada.")

        return jsonify(
            {
                'id': categoria.id,
                'nome': categoria.nome,
                'nomes_produtos': [produto.nome for produto in categoria.produtos] if categoria.produtos else []
            }
        ), 200
    
    except Exception as e:
        abort(500, description=f"Erro ao buscar categoria: {str(e)}")                


@categoria.route('/categorias/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_by_id_categoria(id):
    try:
        categoria = Categoria.query.get(id)

        if not categoria:
            abort(404, description="Categoria não encontrada.")

        db.session.delete(categoria)
        db.session.commit()
        
        return '', 204
    
    except Exception as e:
        abort(500, description=f"Erro ao excluir categoria: {str(e)}")

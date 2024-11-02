from app import db
from app.models.detalhe_pedido import DetalhePedido
from flask import request, jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, validate, ValidationError
from sqlalchemy.orm import joinedload

detalhe_pedido = Blueprint('detalhe_pedidos', __name__)

class DetalhePedidoSchema(Schema):
    id_pedido = fields.String(required=True)
    id_produto = fields.String(required=True)
    valor = fields.Decimal(required=True)
    desconto = fields.Decimal(required=True)

@detalhe_pedido.route('/detalhe_pedidos', methods=['POST'])
@jwt_required()
def create_detalhe_pedido():
    data = request.get_json()
    schema = DetalhePedidoSchema()

    try:
        valida_data = schema.load(data)

        id_pedido = valida_data.get('id_pedido')
        id_produto = valida_data.get('id_produto')
        valor = valida_data.get('valor')
        desconto = valida_data.get('desconto')

        novo_detalhe_pedido = DetalhePedido(id_pedido=id_pedido, id_produto=id_produto, valor=valor, desconto=desconto)

        db.session.add(novo_detalhe_pedido)
        db.session.commit()

        return jsonify(
            {
                'id': novo_detalhe_pedido.id,
                'id_pedido': novo_detalhe_pedido.id_pedido,
                'id_produto': novo_detalhe_pedido.id_produto,
                'valor': novo_detalhe_pedido.valor,
                'desconto': novo_detalhe_pedido.desconto
            }
        ), 201

    except ValidationError as ve:
        abort(400, description=f"Erro na validação dos dados: {ve.messages}")

    except Exception as e:
        abort(500, description=f"Erro no cadastro do detalhe_pedido: {str(e)}")

@detalhe_pedido.route('/detalhe_pedidos/<string:id>', methods=['PUT'])
@jwt_required()
def update_detalhe_pedido(id):
    data = request.get_json()
    schema = DetalhePedidoSchema()

    detalhe_pedido = DetalhePedido.query.get(id)

    if not detalhe_pedido:
        abort(404, description="Detalhe do pedido não encontrado.")

    try:
        valida_data = schema.load(data)

        detalhe_pedido.id_pedido = valida_data.get('id_pedido')
        detalhe_pedido.id_produto = valida_data.get('id_produto')
        detalhe_pedido.valor = valida_data.get('valor')
        detalhe_pedido.desconto = valida_data.get('desconto')

        db.session.commit()

        return jsonify(
            {
                'id': detalhe_pedido.id,
                'id_pedido': detalhe_pedido.id_pedido,
                'id_produto': detalhe_pedido.id_produto,
                'valor': detalhe_pedido.valor,
                'desconto': detalhe_pedido.desconto
            }
        ), 200

    except ValidationError as ve:
        abort(400, description=f"Erro na validação dos dados: {ve.messages}")

    except Exception as e:
        abort(500, description=f"Erro ao atualizar o detalhe_pedido: {str(e)}")

@detalhe_pedido.route('/detalhe_pedidos', methods=['GET'])
@jwt_required()
def get_all_detalhe_pedido():
    try:
        detalhe_pedidos = DetalhePedido.query.all()

        if not detalhe_pedidos:
            abort(404, description="Nenhum detalhe do pedido encontrado.")

        return jsonify([
            {
                'id': detalhe_pedido.id,
                'id_pedido': detalhe_pedido.id_pedido,
                'id_produto': detalhe_pedido.id_produto,
                'valor': detalhe_pedido.valor,
                'desconto': detalhe_pedido.desconto
            } for detalhe_pedido in detalhe_pedidos
        ]), 200

    except Exception as e:
        abort(500, description=f"Erro ao listar detalhes do pedido: {str(e)}")

@detalhe_pedido.route('/detalhe_pedidos/<string:id>', methods=['GET'])
@jwt_required()
def get_by_id_detalhe_pedido(id):
    try:
        detalhe_pedido = DetalhePedido.query.filter_by(id=id).options(
            joinedload(DetalhePedido.pedido),
            joinedload(DetalhePedido.produto)
        ).first()

        if not detalhe_pedido:
            abort(404, description="Detalhe do pedido não encontrado.")

        return jsonify(
            {
                'id': detalhe_pedido.id,
                'id_pedido': detalhe_pedido.id_pedido,
                'id_cliente': detalhe_pedido.pedido.id_cliente if detalhe_pedido.pedido else None,
                'data_compra': detalhe_pedido.pedido.data_compra if detalhe_pedido.pedido else None,
                'id_produto': detalhe_pedido.id_produto,
                'nome_produto': detalhe_pedido.produto.nome if detalhe_pedido.produto else None,
                'valor': detalhe_pedido.valor,
                'desconto': detalhe_pedido.desconto
            }
        ), 200

    except Exception as e:
        abort(500, description=f"Erro ao buscar detalhe do pedido: {str(e)}")

@detalhe_pedido.route('/detalhe_pedidos/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_by_id_detalhe_pedido(id):
    try:
        detalhe_pedido = DetalhePedido.query.get(id)

        if not detalhe_pedido:
            abort(404, description="Detalhe do pedido não encontrado.")

        db.session.delete(detalhe_pedido)
        db.session.commit()

        return '', 204

    except Exception as e:
        abort(500, description=f"Erro ao excluir detalhe do pedido: {str(e)}")

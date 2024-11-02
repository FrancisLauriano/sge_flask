from app import db
from app.models.pedido import Pedido
from flask import request, jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, validate, ValidationError
from sqlalchemy.orm import joinedload

pedido = Blueprint('pedidos', __name__)

class PedidoSchema(Schema):
    id_cliente = fields.String(required=True)

@pedido.route('/pedidos', methods=['POST'])
@jwt_required()
def create_pedido():
    data = request.get_json()
    schema = PedidoSchema() 

    try:
        valida_data = schema.load(data)

        id_cliente = valida_data.get('id_cliente').lower()

        novo_pedido = Pedido(id_cliente=id_cliente)

        db.session.add(novo_pedido)
        db.session.commit()

        return jsonify(
            {
                'id': novo_pedido.id,
                'data_compra': novo_pedido.data_compra,
                'id_cliente': novo_pedido.id_cliente
            }
        ), 201
    
    except ValidationError as ve:
        abort(400, description=f"Erro na validação dos dados: {ve.messages}")

    except Exception as e:
        abort(500, description=f"Erro no cadastro do pedido: {str(e)}")


@pedido.route('/pedidos/<string:id>', methods=['PUT'])
@jwt_required()
def update_pedido(id):
    data = request.get_json()
    schema = PedidoSchema()

    pedido = Pedido.query.get(id)

    if not pedido:
        abort(404, description="Pedido não encontrado.")
    
    try:
        valida_data = schema.load(data)

        id_cliente = valida_data.get('id_cliente').lower()
        pedido.id_cliente = id_cliente

        db.session.commit()

        return jsonify(
            {
                'id': pedido.id,
                'data_compra': pedido.data_compra,
                'id_cliente': pedido.id_cliente
            }
        ), 200
    
    except ValidationError as ve:
        abort(400, description=f"Erro na validação dos dados: {ve.messages}")

    except Exception as e:
        abort(500, description=f"Erro ao atualizar o pedido: {str(e)}")


@pedido.route('/pedidos', methods=['GET'])
@jwt_required()
def get_all_pedido():
    try:
        pedidos = Pedido.query.all()

        if not pedidos:
            abort(404, description="Nenhum pedido encontrado.")

        return jsonify([
            {
                'id': pedido.id,
                'data_compra': pedido.data_compra,
                'id_cliente': pedido.id_cliente
            } for pedido in pedidos
        ]), 200
    
    except Exception as e:
        abort(500, description=f"Erro ao listar pedidos: {str(e)}")        


@pedido.route('/pedidos/<string:id>', methods=['GET'])
@jwt_required()
def get_by_id_pedido(id):
    try:
        pedido = Pedido.query.filter_by(id=id).options(
            joinedload(Pedido.cliente),
            joinedload(Pedido.detalhe_pedido),
        ).first()

        if not pedido:
            abort(404, description="Pedido não encontrado.")

        return jsonify(
            {
                'id': pedido.id,
                'data_compra': pedido.data_compra,
                'id_cliente': pedido.id_cliente,
                'nome_cliente': pedido.cliente.nome if pedido.cliente else None,
                'email_cliente': pedido.cliente.email if pedido.cliente else None,
            }
        ), 200
    
    except Exception as e:
        abort(500, description=f"Erro ao buscar pedido: {str(e)}")                


@pedido.route('/pedidos/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_by_id_pedido(id):
    try:
        pedido = Pedido.query.get(id)

        if not pedido:
            abort(404, description="Pedido não encontrado.")

        db.session.delete(pedido)
        db.session.commit()
        
        return '', 204
    
    except Exception as e:
        abort(500, description=f"Erro ao excluir pedido: {str(e)}")

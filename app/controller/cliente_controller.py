from app import db
from app.models.cliente import Cliente
from flask import request, jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, validate, ValidationError

cliente = Blueprint('clientes', __name__)

class ClienteSchema(Schema):
    nome = fields.String(required=True, validate=validate.Length(min=3, max=255))
    email = fields.Email(required=True, validate=validate.Length(max=255))
    

@cliente.route('/clientes', methods=['POST'])
@jwt_required()
def create_cliente(novo_cliente):
    data = request.get_json()
    schema = ClienteSchema() 

    try:
        valida_data = schema.load(data)

        nome = valida_data.get('nome').lower()
        email = valida_data.get('email').lower()

        if Cliente.query.filter_by(email=email).first():
            abort(400, description="E-mail já está cadastrado.")

        novo_cliente = Cliente(nome=nome, email=email)

        db.session.add(novo_cliente)
        db.session.commit()

        return jsonify(
            {
                'id': novo_cliente.id,
                'nome': novo_cliente.nome,
                'email': novo_cliente.email
            }
        ), 201
    
    except ValidationError as ve:
        abort(400, description=f"Erro na validação dos dados: {ve.messages}")

    except Exception as e:
        abort(500, description=f"Erro no cadastro do cliente: {str(e)}")


@cliente.route('/clientes/<string:id>', methods=['PUT'])
@jwt_required()
def update_cliente(id, cliente):
    data = request.get_json()
    schema = ClienteSchema()

    cliente = Cliente.query.get(id)

    if not cliente:
        abort(404, description="cliente não encontrado.")
    

    try:
        valida_data = schema.load(data)

        nome = valida_data.get('nome').lower()
        email = valida_data.get('email').lower()

        email_existe = Cliente.query.filter_by(email=email).first()
                                               
        if email_existe and email_existe.id != cliente.id:
            abort(400, description="Email já está cadastrado.")

        cliente.nome = nome
        cliente.email = email

        db.session.commit()

        return jsonify(
            {
                'id': cliente.id,
                'nome': cliente.nome,
                'email': cliente.email,
            }
        ), 200
    
    except ValidationError as ve:
        abort(400, description=f"Erro na validação dos dados: {ve.messages}")

    except Exception as e:
        abort(500, description=f"Erro ao atualizar do cliente: {str(e)}")


@cliente.route('/clientes', methods=['GET'])
@jwt_required()
def get_all_cliente():
    try:
        clientes = Cliente.query.all()

        if not clientes:
            abort(404, description="Nenhum cliente encontrado.")

        
        return jsonify([
            {
                'id': cliente.id,
                'nome': cliente.nome,
                'email': cliente.email
            } for cliente in clientes
        ]), 200
    
   
    except Exception as e:
        abort(500, description=f"Erro ao listar clientes: {str(e)}")        


@cliente.route('/clientes/<string:id>', methods=['GET'])
@jwt_required()
def get_by_id_cliente(id):
    try:
        cliente = Cliente.query.get(id)

        if not cliente:
            abort(404, description="cliente não encontrado.")

        
        return jsonify(
            {
                'id': cliente.id,
                'nome': cliente.nome,
                'email': cliente.email
            }
        ), 200
    
   
    except Exception as e:
        abort(500, description=f"Erro ao buscar cliente: {str(e)}")                


@cliente.route('/clientes/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_by_id_cliente(id):
    try:
        cliente = Cliente.query.get(id)

        if not cliente:
            abort(404, description="cliente não encontrado.")

        db.session.delete(cliente)
        db.session.commit()
        
        return '', 204
    
    except Exception as e:
        abort(500, description=f"Erro ao excluir cliente: {str(e)}")                        
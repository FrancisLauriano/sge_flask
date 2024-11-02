from app import db
from app.models.usuario import Usuario
from flask import request, jsonify, abort, Blueprint
from app.utils.encryption import Encryption
from app.utils.jwt_manager import JWTManager
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, validate, ValidationError

usuario = Blueprint('usuarios', __name__)


class UsuarioSchema(Schema):
    nome = fields.String(required=True, validate=validate.Length(min=3, max=255))
    email = fields.Email(required=True, validate=validate.Length(max=255))
    senha = fields.String(
        required=True,
        validate=validate.Length(min=6, max=10)
    )


@usuario.route('/login', methods=['POST'])
def login(self, email, senha):
    try:
        data = request.get_json()
        email = data.get('email').lower()
        senha = data.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            abort(404, description="Usuário não encontrado.")

        if not self.encryption.decrypt(usuario.senha) == senha:
            abort(401, description="Senha inválida.")

        token = JWTManager.create_token({"id": str(usuario.id)})
        return jsonify({"token": token}), 200
    except Exception as e:
        abort(404, description=f"Erro ao realizar login: {str(e)}")


@usuario.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    schema = UsuarioSchema()

    try:
        valida_data = schema.load(data)

        nome = valida_data.get('nome').lower()
        email = valida_data.get('email').lower()
        senha = valida_data.get('senha')
        
        if Usuario.query.filter_by(email=email).first():
            abort(400, description="E-mail já está cadastrado.")

        encrypted_senha = Encryption().encrypt(senha)

        novo_usuario = Usuario(nome=nome, email=email, senha=encrypted_senha)

        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify(
            {
                'id': novo_usuario.id,
                'nome': novo_usuario.nome,
                'email': novo_usuario.email,
                'senha': novo_usuario.senha,
                'data_cadastro': novo_usuario.data_cadastro
            }
        ), 201
    
    except ValidationError as ve:
        abort(400, description=f"Erro na validação dos dados: {ve.messages}")

    except Exception as e:
        abort(500, description=f"Erro no cadastro do usuário: {str(e)}")


@usuario.route('/usuarios/<string:id>', methods=['PUT'])
@jwt_required()
def update_usuario(id):
    data = request.get_json()
    schema = UsuarioSchema()

    usuario = Usuario.query.get(id)

    if not usuario:
        abort(404, description="Usuário não encontrado.")
    

    try:
        valida_data = schema.load(data)

        nome = valida_data.get('nome').lower()
        email = valida_data.get('email').lower()
        senha = valida_data.get('senha')

        email_existe = Usuario.query.filter_by(email=email).first()
                                               
        if email_existe and email_existe.id != usuario.id:
            abort(400, description="Email já está cadastrado.")

        encrypted_senha = Encryption().encrypt(senha)

        usuario.nome = nome
        usuario.email = email
        usuario.senha = encrypted_senha

        db.session.commit()

        return jsonify(
            {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'senha': usuario.senha,
                'data_cadastro': usuario.data_cadastro
            }
        ), 200
    
    except ValidationError as ve:
        abort(400, description=f"Erro na validação dos dados: {ve.messages}")

    except Exception as e:
        abort(500, description=f"Erro ao atualizar do usuário: {str(e)}")


@usuario.route('/usuarios', methods=['GET'])
@jwt_required()
def get_all_usuario():
    try:
        usuarios = Usuario.query.all()

        if not usuarios:
            abort(404, description="Nenhum usuário encontrado.")

        
        return jsonify([
            {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'data_cadastro': usuario.data_cadastro
            } for usuario in usuarios
        ]), 200
    
   
    except Exception as e:
        abort(500, description=f"Erro ao listar usuários: {str(e)}")        


@usuario.route('/usuarios/<string:id>', methods=['GET'])
@jwt_required()
def get_by_id_usuario(id):
    try:
        usuario = Usuario.query.get(id)

        if not usuario:
            abort(404, description="Usuário não encontrado.")

        
        return jsonify(
            {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'data_cadastro': usuario.data_cadastro
            }
        ), 200
    
   
    except Exception as e:
        abort(500, description=f"Erro ao buscar usuário: {str(e)}")                


@usuario.route('/usuarios/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_by_id_usuario(id):
    try:
        usuario = Usuario.query.get(id)

        if not usuario:
            abort(404, description="Usuário não encontrado.")

        db.session.delete(usuario)
        db.session.commit()
        
        return '', 204
   
    except Exception as e:
        abort(500, description=f"Erro ao excluir usuário: {str(e)}")                        
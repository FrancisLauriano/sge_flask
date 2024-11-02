from flask import request, jsonify
from functools import wraps
from app.utils.jwt_manager import JWTManager
from app.models.usuario import Usuario

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token é obrigatório'}), 401

        try:
            token_data = JWTManager.decode_token(token.split()[1])
            request.user = Usuario.query.get(token_data['data']['id'])
        except Exception as e:
            return jsonify({'message': str(e)}), 401

        return f(*args, **kwargs)
    return decorated
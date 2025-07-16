from flask import Blueprint, request, jsonify
from app.models import Admin
from .. import db

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    admin = Admin.query.filter_by(email=email).first()

    if admin and admin.check_password(password):
        return jsonify({'message': 'Login berhasil', 'email': email}), 200
    else:
        return jsonify({'message': 'Login gagal'}), 401

from flask import Blueprint, request
from app.controllers.user_controller import register_user, login_user

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data)


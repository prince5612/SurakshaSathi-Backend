from flask import jsonify
from app import bcrypt, get_db
from flask_jwt_extended import create_access_token

def register_user(data):
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    print("s")
    if not name or not email or not password:
        return jsonify({"message": "Name, email, and password are required"}), 400

    db = get_db()
    user_collection = db["users"]

    # Check if a user with the given email already exists
    if user_collection.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    result = user_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed_pw
    })

    user_id = str(result.inserted_id)
    token = create_access_token(identity=user_id)

    return jsonify({"id": user_id, "name": name, "email": email, "token": token}), 201

def login_user(data):
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    db = get_db()
    user = db["users"].find_one({"email": email})

    if user and bcrypt.check_password_hash(user['password'], password):
        token = create_access_token(identity=str(user['_id']))
        return jsonify({
            "id": str(user['_id']),
            "name": user['name'],
            "email": user['email'],
            "token": token
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

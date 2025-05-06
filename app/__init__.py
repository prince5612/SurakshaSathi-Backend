from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from pymongo import MongoClient
import urllib.parse
import os

bcrypt = Bcrypt()
jwt = JWTManager()

mongo = None  # Global Mongo client

def create_app():
    global mongo
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    bcrypt.init_app(app)
    jwt.init_app(app)

    # MongoDB setup
    username = os.getenv('MONGO_USER')
    password = os.getenv('MONGO_PASSWORD')
    username_esc = urllib.parse.quote_plus(username)
    password_esc = urllib.parse.quote_plus(password)
    MONGO_URI = f"mongodb+srv://{username_esc}:{password_esc}@surakshasathi.d2azkdd.mongodb.net/?retryWrites=true&w=majority&appName=SurakshaSathi"
    
    if not MONGO_URI:
        raise RuntimeError("MONGO_URI is required")

    mongo = MongoClient(MONGO_URI)

    from app.routes.user_routes import user_bp
    

    app.register_blueprint(user_bp, url_prefix="/api/users")
    
    from app.routes.insurance_routes import insurance_bp
    app.register_blueprint(insurance_bp,url_prefix="/api/insurance")

    return app

def get_db():
    return mongo["SurkshaSathi"]

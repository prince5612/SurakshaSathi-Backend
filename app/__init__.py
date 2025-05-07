from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from pymongo import MongoClient
import urllib.parse
import os
from flask_mail import Mail

bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()
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

    app.config.update(
        MAIL_SERVER=os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
        MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
        MAIL_USE_TLS=True,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=('SurakshaSathi', os.getenv('MAIL_USERNAME'))
    )
    mail.init_app(app)

    # UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
    # os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

    from app.routes.user_routes import user_bp
    

    app.register_blueprint(user_bp, url_prefix="/api/users")
    
    from app.routes.insurance_routes import insurance_bp
    app.register_blueprint(insurance_bp,url_prefix="/api/insurance")

    from app.routes.notifications_routes import notif_bp
    app.register_blueprint(notif_bp,url_prefix="/api/notif")
    return app

def get_db():
    return mongo["SurkshaSathi"]

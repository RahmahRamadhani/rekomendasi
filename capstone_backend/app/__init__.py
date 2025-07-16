from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from app.routes.rekomendasi import rekomendasi_bp
    from app.routes.admin import admin_bp
    from app.routes.pekerjaan import pekerjaan_bp

    app.register_blueprint(rekomendasi_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(pekerjaan_bp)

    return app

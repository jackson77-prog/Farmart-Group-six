from flask import Flask
from .config import Config
from .models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from .routes import api_bp
    app.register_blueprint(api_bp)

    return app

app = create_app()

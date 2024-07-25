from flask import Flask
from server.models import db
from server.routes import api_bp
from server.config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database with the app
db.init_app(app)
migrate = Migrate(app, db)

# Register the Blueprint with the URL prefix
app.register_blueprint(api_bp)

# Error handler for better debugging
@app.errorhandler(Exception)
def handle_exception(e):
    return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

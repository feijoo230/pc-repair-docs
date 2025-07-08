import os # Importamos 'os' para construir rutas de forma segura
from flask import Flask
from .routes import main
from .models import connect_to_mongo

def create_app():
    
    app = Flask(__name__, static_folder='../static')


    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, '../static/uploads')
    
    app.config.from_envvar("FLASK_ENV", silent=True) 

    connect_to_mongo()
    app.register_blueprint(main)

    return app
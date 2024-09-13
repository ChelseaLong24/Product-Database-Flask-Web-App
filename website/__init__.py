import os
from flask import Flask
import pandas as pd
#from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'kskidjd kdk'

    basedir = os.path.abspath(os.path.dirname(__file__))
    excel_file = os.path.join(basedir, 'data.xlsx')

    data = pd.read_excel(excel_file)
    app.config['DATA'] = data

    from .views import views
   
    app.register_blueprint(views, url_prefix = '/') #slash means no prefix
    
    return app
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

def create_app():
    from .views.query import Query
    
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Query, '/predict')
    CORS(app)
    return app

__all__ = ['create_app']
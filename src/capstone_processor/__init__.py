from flask import Flask
from flask_restful import Api

def create_app():
    from .views.query import Query
    
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Query, '/predict')
    return app

__all__ = ['create_app']
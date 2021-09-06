from flask import request
from flask_restful import Resource,Api
from flask import Flask
from typing import Dict
from flask import Flask


def create_app(config_dict: Dict = {}):
    app = Flask(__name__)    
    return app

class HealthCheck(Resource):   

    def get(self):
        data={
            "echo" : "ok"
        }
        return data



app = create_app()
app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(HealthCheck, "/healthcheck")



if __name__ == '__main__':
    app.run()
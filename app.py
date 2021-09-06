from flask_apscheduler import APScheduler
from datetime import datetime
import redis
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
            "StartTime" : str(redisInstance.get("StartTime")),
            "LastQuery" : str(redisInstance.get("LastQuery"))
        }
        return data


redisInstance = redis.Redis(
    host='ec2-52-73-185-231.compute-1.amazonaws.com', 
    port=17030,
    password="p8246bd54e4335f5d4001090409c247e242ebbc0d28a3a9a8f92400e7b9e1d178",
    ssl=True,
    ssl_cert_reqs=None
    )

startTime=datetime.now()
redisInstance.set('StartTime', str(startTime))

app = create_app()
app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(HealthCheck, "/healthcheck")

scheduler = APScheduler()

@scheduler.task('interval', id='do_job_1', seconds=30, misfire_grace_time=900)
def job1():
    LastQuery=datetime.now()
    redisInstance.set('LastQuery', str(LastQuery))    

scheduler.start()


if __name__ == '__main__':
    app.run()
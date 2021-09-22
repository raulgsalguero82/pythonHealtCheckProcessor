from urllib.error import HTTPError
import requests
import urllib.request
import json
from flask_apscheduler import APScheduler
from datetime import datetime
import redis
from flask import request
from flask_restful import Resource,Api
from flask import Flask
from typing import Dict
from flask import Flask
from flask_cors import CORS



def create_app(config_dict: Dict = {}):
    app = Flask(__name__)    
    return app

class HealthCheck(Resource):   

    def get(self):
        nodes=json.loads(redisInstance.get("Nodes"))
        lastStatus=json.loads(redisInstance.get("LastStatus"))

        data={
            "StartTime" : str(redisInstance.get("StartTime")),
            "LastQuery" : str(redisInstance.get("LastQuery")),
            "Nodes" : nodes ,
            "LastStatus":  lastStatus
        }
        return data


redisInstance = redis.Redis(
    host='ec2-50-19-196-205.compute-1.amazonaws.com', 
    port=17830,
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
CORS(app)

scheduler = APScheduler()

@scheduler.task('interval', id='do_job_1', seconds=10, misfire_grace_time=900)
def job1():
    LastQuery=datetime.now()
    redisInstance.set('LastQuery', str(LastQuery))    
    nodesString=redisInstance.get('Nodes')        
    nodes_list= []
    nodes_list.append(json.loads(nodesString))        
    response=[]
    
    for node in nodes_list[0]:        
        code,elapsed=getResponseCode(str(node["url"]))
        print(node["url"] +"-"+str(code)+"-"+str(elapsed) )
        nodeStatus=""
        if(code==200):
            nodeStatus="Active"
        else:
            nodeStatus="InActive"
        nodeResponse={ "name" : str(node["name"]) , "status" : nodeStatus,"elapsed" : str(elapsed), "lastStatusCode" : code}
        response.append( nodeResponse)

    redisInstance.set('LastStatus',json.dumps(response))


def getResponseCode(url):
    try:
        response = requests.get(url)
        return response.status_code, response.elapsed        
    except requests.exceptions.HTTPError as err:
        return err.response.status_code,0


scheduler.start()


if __name__ == '__main__':
    app.run()
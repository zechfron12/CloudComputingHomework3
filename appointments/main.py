from flask import Flask, request, jsonify
import requests
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from cfg import url
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
api = Api(app)


class Appointments(Resource):
    def get(self):
        req = requests.get(url)
        return req.text

    def post(self):
        req_body = request.get_json()
        req = requests.post(
            url, json=req_body)
        if req.status_code == 200:
            resp = jsonify(req.json())
        else:
            resp = jsonify(req.text)
        resp.status_code = req.status_code

        return resp

    def delete(self):
        req_body = request.get_json()
        req = requests.delete(
            url, json=req_body)

        resp = jsonify(req.text)
        resp.status_code = req.status_code

        return resp


api.add_resource(Appointments, '/appointments')

if __name__ == '__main__':
    app.run()

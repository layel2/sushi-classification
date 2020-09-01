import json
import time
from flask import Flask
from flask_restful import Resource,Api,reqparse
import requests
import sushi_pred

app = Flask(__name__)
api = Api(app=app)

@app.route('/')
def index():
	return "Layyer"

class callAPI(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('imgurl',type=str)
		dictp = parser.parse_args()
		ret = sushi_pred.urlpred(dictp['imgurl'])
		#print(ret)
		return ret

api.add_resource(callAPI,'/callAPI',endpoint='getAPI')

if __name__ == '__main__':
	app.run(threaded=True)
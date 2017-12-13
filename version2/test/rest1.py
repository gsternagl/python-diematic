from flask import Flask, request
from flask_restful import Resource, Api
  
app = Flask(__name__)
api = Api(app)

class Locator1(Resource):
  def get(self):
    s = "Pappnase"
    return s

class Locator2(Resource):
  def get(self, arg):
    s = "Locator2: " + arg
    return s
 
  
api.add_resource(Locator2, '/registers/<string:arg>')
api.add_resource(Locator1, '/registers')

if __name__ == '__main__':
  app.run()

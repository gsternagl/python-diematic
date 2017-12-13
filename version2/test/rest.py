from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps

class restApp:
  regs = {}
  
  class Locator1(Resource):
    def get(self):
      s = json.dumps(restApp.regs)
      return s

  class Locator2(Resource):
    def get(self, arg):
      s = "Locator2: " + arg
      return s
 
  def __init__(self):
    app = Flask(__name__)
    api = Api(app)
    self.setRegisters()
    api.add_resource(self.Locator2, '/registers/<string:arg>')
    api.add_resource(self.Locator1, '/registers')
    app.run()

  def setRegisters(self):
    s = {'reg_name': 'TEMP', \
         'reg_cont': ( { 'reg_val': '10.0', \
                         'reg_min': '0.0', \
                         'reg_max': '100.0', } ) }
    self.regs.update(s)



if __name__ == '__main__':
  foo = restApp() 

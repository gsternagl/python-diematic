#!flask/bin/python

from app import app
app.run(port=5001, debug=app.config['DEBUG'])

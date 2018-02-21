#!flask/bin/python

from app import app
app.run(port=app.config['DIEMATICD_PORT'], debug=app.config['FLASK_DEBUG'])

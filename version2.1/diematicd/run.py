#!/usr/bin/python3

from app import app
app.run(host='0.0.0.0', port=app.config['DIEMATICD_PORT'], debug=app.config['FLASK_DEBUG'])

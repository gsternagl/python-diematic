#!flask/bin/python

from app import app

if __name__ == "__main__":
    app.run(port=5001, debug=app.config['DEBUG'])

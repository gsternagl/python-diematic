import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# get bootstrap files from local filesystem instead of CDN
BOOTSTRAP_SERVE_LOCAL = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
SECRET_KEY = 'ich-bin-strenggeheim'
#DEBUG = False
DEBUG = True

# DiematicD settings
#DIEMATICD_EMULATION = False
DIEMATICD_EMULATION = True
DIEMATICD_HOST = '192.168.178.21'
DIEMATICD_PORT = 5000

# InfluxDB parameters for timeseries data
INFLUX_EMULATION = True
#INFLUX_EMULATION = False
INFLUX_HOST = '192.168.178.106'
INFLUX_PORT = 8086
INFLUX_USER = 'root'
INFLUX_PW = 'root'
INFLUX_DBNAME = 'diematic'
INFLUX_METRIC = 'temperatures'

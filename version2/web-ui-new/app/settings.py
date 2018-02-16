class MySettings():

    def __init__(self, app):
        self.influxdb_host  = app.config['INFLUX_HOST']
        self.influxdb_port  = app.config['INFLUX_PORT']
        self.influxdb_db    = app.config['INFLUX_DBNAME']
        self.influxdb_table = app.config['INFLUX_METRIC']
        self.influxdb_user  = app.config['INFLUX_USER']
        self.influxdb_pw    = app.config['INFLUX_PW']
        self.diematicd_host = app.config['DIEMATICD_HOST']
        self.diematicd_port = app.config['DIEMATICD_PORT']

    def update(self, app, 
        influxdb_host,
        influxdb_port,
        influxdb_db,
        influxdb_table,
        influxdb_user,
        influxdb_pw,
        diematicd_host,
        diematicd_port):

        self.influxdb_host  = app.config['INFLUX_HOST']    = influxdb_host
        self.influxdb_port  = app.config['INFLUX_PORT']    = influxdb_port
        self.influxdb_db    = app.config['INFLUX_DBNAME']  = influxdb_db
        self.influxdb_table = app.config['INFLUX_METRIC']  = influxdb_table
        self.influxdb_user  = app.config['INFLUX_USER']    = influxdb_user
        self.influxdb_pw    = app.config['INFLUX_PW']      = influxdb_pw
        self.diematicd_host = app.config['DIEMATICD_HOST'] = diematicd_host
        self.diematicd_port = app.config['DIEMATICD_PORT'] = diematicd_port


from influxdb import InfluxDBClient
from datetime import datetime, date, time


class Chart(object):
    def __init__(self, app):
        try:
            self.INFLUX_EMULATION = app.config['INFLUX_EMULATION']
            self.INFLUX_HOST = app.config['INFLUX_HOST']
            self.INFLUX_PORT = app.config['INFLUX_PORT']
            self.INFLUX_USER = app.config['INFLUX_USER']
            self.INFLUX_PW = app.config['INFLUX_PW']
            self.INFLUX_DBNAME = app.config['INFLUX_DBNAME']
            self.INFLUX_METRIC = app.config['INFLUX_METRIC']
        except:
            print("Configuration File is missing some Influx settings")


    def get_data(self, time_span, show_gaps):
        data_values1 = []
        data_values2 = []
        data_values3 = []
        data_labels = []

        if not self.INFLUX_EMULATION:
            client = InfluxDBClient(
                self.INFLUX_HOST,
                self.INFLUX_PORT,
                self.INFLUX_USER,
                self.INFLUX_PW,
                self.INFLUX_DBNAME
            )
            if client is not None:
                # if show_gaps True then change fill option to get 0 values
                fill = '0' if show_gaps else 'none'

                query = 'SELECT mean(temp_ext), mean(temp_ecs), ' + \
                        'mean(temp_boiler) ' + \
                        'FROM {} WHERE '.format(self.INFLUX_METRIC) + \
                        'time > now() - {} '.format(time_span) + \
                        'GROUP BY time(1m) fill({})'.format(fill)

                try:
                    result = client.query(query, database=self.INFLUX_DBNAME)
                except:
                    print 'InfluxDB query failed'
                    return [], [], [], []

                if result is not None:
                    points = list(result.get_points(measurement='temperatures'))

                    for point in points:
                        thetime = datetime.strptime(point['time'], '%Y-%m-%dT%H:%M:%SZ')
                        mytime = thetime.strftime('%Y-%m-%d %H:%M:%S')
                        val1 = val2 = val3 = None
                        has_gap = True
                        try:
                            if point['mean'] is not None:
                                val1 = point['mean']
                                val2 = point['mean_1']
                                val3 = point['mean_2']
                                has_gap = False

                        except Exception as inst:
                            pass

                        if not has_gap:
                            data_labels.append(mytime)
                            data_values1.append(val1)
                            data_values2.append(val2)
                            data_values3.append(val3)

        # InfluxDB Emulation mode
        # fill list with some predefined values
        else:
            timespans = {'1h': 60*60, '2h': 60*60*2, \
                         '6h': 60*60*6, '12h': 60*60*12, \
                         '1d': 60*60*24, '7d': 60*60*24*7}
            val1 = [10, 11, 13, 14, 13, 12, 10]
            val2 = [40, 41, 43, 45, 43, 42, 40]
            val3 = [60, 62, 70, 75, 70, 65, 60]
            len_sec = timespans[time_span]
            end_time = int(datetime.now().strftime('%s'))
            curr_time = end_time - len_sec
            # 7 values per 1 hour
            interval = 3600 / 7
            while curr_time < end_time:
                data_labels.append(datetime.fromtimestamp(curr_time).strftime('%Y-%m-%d %H:%M:%S'))
                data_values1.extend(val1)
                data_values2.extend(val2)
                data_values3.extend(val3)
                curr_time += interval

        return data_values1, data_values2, data_values3, data_labels

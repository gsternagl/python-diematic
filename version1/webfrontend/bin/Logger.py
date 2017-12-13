import datetime

class Logger(object):
  def log(self, message):
    print message

class TimestampLogger(Logger):
  def log(self, message):
    message = "{ts} {msg}".format(ts=datetime.datetime.now(), msg=message)
    super(TimestampLogger, self).log(message)

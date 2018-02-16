mydata = { \
            "DAY":    [ int(self.ctrl_date.day) ], \
            "MONTH":  [ int(self.ctrl_date.month) ], \
            "HOUR":   [ int(self.ctrl_date.time[0:2]) ], \
            "MINUTE": [ int(self.ctrl_date.time[3:5]) ] \
        }

print mydata

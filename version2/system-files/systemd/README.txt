To start diematicd automatically on Linux with systemd copy the file diematicd.service to /lib/systemd/system

Then reload systemd files
# systemctl daemon-reload

Enable
# systemctl enable diematicd.service

Start
# systemctl start diematicd.service

List status
# systemctl status diematicd.service

Should look like this:
● diematicd.service - Diematic Daemon
   Loaded: loaded (/lib/systemd/system/diematicd.service; enabled)
   Active: active (running) since Sat 2018-02-03 19:13:22 CET; 3min 40s ago
 Main PID: 1305 (python)
   CGroup: /system.slice/diematicd.service
           ├─1305 /usr/bin/python /root/src/python/diematic/diematicd/diematicd...
           └─1309 /usr/bin/python /root/src/python/diematic/diematicd/diematicd...

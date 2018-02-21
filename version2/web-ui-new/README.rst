Diematic Web-UI and Admin-UI based on flask
===========================================
For development the required python libraries are stored in a virtualenv
in directory ./flask. For production this can be replaced by system-wide 
python packages

for local testing start with:

* ./run_dev.py

This outputs the URL which you can connect to using a web-browser. 
It's usually: <http://0.0.0.0:5001>

You need a use login to access the UI. The user accounts can be managed with
another Flask-application called "admin_ui". 

You can start this (not concurrently with the Web-UI as they are using the same port 5001) by doing:

* ./run_admin_dev.py

Also connect to <http://0.0.0.0:5001>

Setting it up for production
----------------------------

For "production" I recommend using the gunicorn WSGI server and NGINX. I have included the relevant systemd files for gunicorn and a config file for NGINX here in the same directory. 
The setup I have used was a "gunicorn.socket" systemd-service which is enabled and started via systemd. This service would then automatically start another service called "gunicorn.service" which in fact starts the gunicorn server which starts the actual python-script "run.py".

Note that gunicorn communicates with NGINX via unix-sockets and you must enable systemd to create sockets in /run/gunicorn. You can do this by creating a file "/etc/tmpfiles.d/gunicorn.conf" with the following content::

  d /run/gunicorn 0755 <user-name> <group-name> -


I wouldn't recommend to expose the admin_ui via NGINX for security reasons and also because you typically won't be using it that often.

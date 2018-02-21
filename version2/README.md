# python-diematic

Version: 2.0 February 2018

# Goal: enable internet connectivity for older RS485-based DeDietrich Diematic 3 Heating controllers.

python-diematic is a python program to control Diematic 3 oil-heater controllers through a RS485 connection remotely. Diematic controllers have a built-in RS485 interface which can be wired to any RS485 2-wire interface on a PC, Raspberry Pi or similar running Linux. Diematic RS485 interfaces use a modified Modbus protocol. Unfortunately I couldn't get any of the existing Modbus python libraries to work with the Diematic so I used an existing project which was implemented in PHP.

http://www.dom-ip.com/wiki/R%C3%A9alisation_d'une_Interface_Web_pour_une_chaudi%C3%A8re_De_Dietrich_%C3%A9quip%C3%A9e_d'une_r%C3%A9gulation_Diematic_3

Largerly my Python implementation is a rewrite of the existing PHP code. I have started this as a self-study project to improve my python skills. The program is normally used with the little web-interface using the web.py framework but you can also just use the core code without the web-interface to dump the Modbus Diematic registers (look in tools directory for example).

# Requirements:

a computer running Linux and Python (preferably a Raspberry Pi) or any UNIX-based computer with Python 2.7
a RS-485 Interface card (e.g. USR-TCP232-24) https://www.amazon.de/Cablematic-Modul-T24-RS232-RS485-Modell-Ethernet-usr-tcp232/dp/B017C7HPW4/ref=sr_1_1?ie=UTF8&qid=1505822120&sr=8-1&keywords=USR-TCP232-24
or alternatively this simple RS485 piggyback board which connects to the RPi's GPIO pins. https://www.conrad.de/de/raspberry-pi-erweiterungs-platine-rb-rs485-1267832.html
I recommend to also look on ebay for these as you might be able to the same devices cheaper there. There are also some compatible variants available which use the same IP-based or serial interface. For the TCP-USR boards you do have to set their network configuration up once via some Windows software. Once you have done that they can be access like a serial interface but you use the socket API to communicate to them.

The Diematic has a range of Modbus registers which slightly differ from model to model and they are not documented publicy. So you have to try out what works for you. I implemented to get and set temperatures and heating curves for my two heating circuits and the warm-water temperature only at the moment but it can be extended.

# Version 2 Changes:

In this release I have switched from an integrated web-interface / diematic comms approach to a separate one. There are now two components:

# 1. diematicd:
A Rest-API based background daemon which provides diematic register values on demand and can also set them individually. I used flask for the Rest-API implementation.

# 2. web-gui
A Flask-based web-application which can read and write values from diematicd via Rest-API and represent them in a modern Web-UI style.

I have not yet converted this to be used in "production" which would probably require a different web-server than the python/flask builtin-one like e.g. Gunicorn + NGINX but plan to do that as soon as the diematicd and web-UI have stabilized.

# HOWTO run:

diematicd and the web-ui can be deployed on 2 different servers but can also be co-located in the same server. I currently have diematicd running on a RPI and the web-ui runs in a VM on my NAS-box.

# diematicd:
diematicd needs a dedicated port to communicate with the web-UI. Currently this is set in diematicd.py via the "app.run(port=5000)" method. If you want another port then change this in the source code as diematicd does not yet have a configuration file. This daemon should run all the time in the background so it might be best to start it via systemd. Don't forget to provide the required python packages. For development I use virtualenv but for deployment installing system-wide packages should be preferred.

run it::
/# cd version2
/# python diematicd.py

# web-ui: 
Use the new package in directory "version2/web-ui-new". There is also a virtualenv setup for development in the sub-directory "flask". For deployment it's better to install the required python packages globally.

There is a configuration file called config.py which you can change with a text editor. The most important settings are die IP-address and port of the "diematicd" and the port address of the web-server itself. 

The virtualenv is for OSX. So you might just want to replace it by ::
/# cd version2/web-ui-new
/# rm -rf flask
/# virtualenv flask
/# source flask/bin/activate
/# pip install -r requirements.txt

The web-ui can be started with::
/# python run_dev.py

Connect your browser to http://0.0.0.0:5001

The port address can also be changed in "version2/web-ui-new/run.py" in the method "app.run()" right at the end.

Befor you can login you need to register a new user. The security model is not yet fully implemented. Just use "register" in the UI to create a new user and then login with that user.

# InfluxDB
I have started using InfluxDB to store my heating's measures and there is a simple charts module in the web-ui which displays these values. My InfluxDB database is running on a VM and I use a little python script "version2/influxDB/aufz-diem-influx.py" which gets values from "diematicd" every 30 sec and writes them into InfluxDB. 

There are also some settings for the web-ui how to access the InfluxDB server in "version2/web-ui-new/config.py"

If you don't want to use InfluxDB you can switch it off by setting INFLUXDB_EMULATION = True in "version2/web-ui-new/config.py". The charts will then show some testing measures.

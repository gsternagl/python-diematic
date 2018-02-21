python-diematic
===============

*Version: 2.0beta Feb-2018*

Goal
----
enable internet connectivity for older RS485-based DeDietrich Diematic 3 Heating controllers.

python-diematic is a python program to control Diematic 3 oil-heater controllers through a RS485 connection remotely. Diematic controllers have a built-in RS485 interface which can be wired to any RS485 2-wire interface on a PC, Raspberry Pi or similar running Linux. Diematic RS485 interfaces use a modified Modbus protocol. Unfortunately I couldn't get any of the existing Modbus python libraries to work with the Diematic so I used an existing project which was implemented in PHP.

http://www.dom-ip.com/wiki/R%C3%A9alisation_d'une_Interface_Web_pour_une_chaudi%C3%A8re_De_Dietrich_%C3%A9quip%C3%A9e_d'une_r%C3%A9gulation_Diematic_3

Largerly my Python implementation is a rewrite of the existing PHP code. I have started this as a self-study project to improve my python skills. The program is normally used with the little web-interface using the web.py framework but you can also just use the core code without the web-interface to dump the Modbus Diematic registers (look in tools directory for example).

Requirements
------------

a computer running Linux and Python (preferably a Raspberry Pi) or any UNIX-based computer with Python 2.7
a RS-485 Interface card (e.g. USR-TCP232-24) https://www.amazon.de/Cablematic-Modul-T24-RS232-RS485-Modell-Ethernet-usr-tcp232/dp/B017C7HPW4/ref=sr_1_1?ie=UTF8&qid=1505822120&sr=8-1&keywords=USR-TCP232-24
or alternatively this simple RS485 piggyback board which connects to the RPi's GPIO pins. https://www.conrad.de/de/raspberry-pi-erweiterungs-platine-rb-rs485-1267832.html
I recommend to also look on ebay for these as you might be able to the same devices cheaper there. There are also some compatible variants available which use the same IP-based or serial interface. For the TCP-USR boards you do have to set their network configuration up once via some Windows software. Once you have done that they can be access like a serial interface but you use the socket API to communicate to them.

The Diematic has a range of Modbus registers which slightly differ from model to model and they are not documented publicy. So you have to try out what works for you. I implemented to get and set temperatures and heating curves for my two heating circuits and the warm-water temperature only at the moment but it can be extended.

For testing I recommend to stick to the CLI version or to start the web.py interface from command-line and then use the webbrowser for the GUI. For "production" I recommend to setup a simple web-server which starts the web.py main application.

Version1
--------

This is what I am currently using "in production" and it should be fully functional. This version consists only of one module which is the web.py based Webgui. All communication to the Diematic Controller is triggered by calling methods of the Diematic class from bin/app.py which is the main web.py application.

For further details look at the README.md file in the version1 directory

Version2
--------
I have recently started to work on a new app-architecture where the communication module runs separately as a daemon and the webui is another process, potentially on any other machine. The moduls talk to each other via Rest API with JSON as a data format. I have used the Flask framework for the Rest API and am currently working to change the existing WebUI from using the web.py framework towards also using Flask instead. This makes it easier for me to maintain.

See in *version2/README.rst* for more information.


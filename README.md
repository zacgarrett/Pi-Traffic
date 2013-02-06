Pi-Traffic
==========
This is a car monitoring script that runs on a raspberry pi. 

Project Goal
------------

The goal for this project is to create a csv file which will be served up via nginx (or another light weight web server) and can then be processed on another machine. 

Hardware Requirements
---------------------

* Raspberry pi
* [Raspberry pi proto plate](http://www.adafruit.com/products/801) -- allows you to build directly on top of the raspberry pi, such as you would with the arduino
* [MCP3008](https://www.adafruit.com/products/856) -- Gives the raspberry pi analog input
* Differential pressure sensor (I used [Freescale MPX5500DP](http://www.digikey.com/scripts/DkSearch/dksus.dll?WT.z_header=search_go&lang=en&keywords=MPX5500DP-ND&x=0&y=0&cur=USD))
* Tubing to fit the pressure sensor

Setting up the Raspberry Pi
---------------------------

    sudo apt-get update
    sudo apt-get install python-dev
    sudo apt-get install python-setuptools
    sudo easy_install rpi.gpio
